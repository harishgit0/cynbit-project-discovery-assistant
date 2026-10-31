from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.inquiry import InquiryCreate
from app.services.briefs import generate_project_brief
from app.services.inquiries import save_inquiry


@pytest.fixture
def valid_payload():
    return {
        "full_name": "Asha Test",
        "email": "asha@example.com",
        "project_category": "ai_automation",
        "project_title": "Support assistant",
        "problem_statement": "Customer questions take too long to answer manually.",
        "objective": "Reduce time spent on routine questions.",
        "requirements": ["AI chatbot or virtual assistant"],
        "budget_range": "Below ₹25,000",
        "expected_timeline": "1–2 months",
        "project_stage": "Idea stage",
    }


def test_inquiry_accepts_valid_data_and_strips_whitespace(valid_payload):
    valid_payload["full_name"] = "  Asha Test  "
    inquiry = InquiryCreate.model_validate(valid_payload)

    assert inquiry.full_name == "Asha Test"
    assert inquiry.project_category == "ai_automation"


def test_inquiry_requires_a_requirement_or_other_text(valid_payload):
    valid_payload["requirements"] = []

    with pytest.raises(ValidationError, match="Select at least one requirement"):
        InquiryCreate.model_validate(valid_payload)


def test_inquiry_rejects_requirement_from_another_category(valid_payload):
    valid_payload["requirements"] = ["Responsive web application"]

    with pytest.raises(ValidationError, match="not available for this category"):
        InquiryCreate.model_validate(valid_payload)


def test_inquiry_rejects_duplicate_requirements(valid_payload):
    valid_payload["requirements"] = [
        "AI chatbot or virtual assistant",
        "AI chatbot or virtual assistant",
    ]

    with pytest.raises(ValidationError, match="only be selected once"):
        InquiryCreate.model_validate(valid_payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("budget_range", "A lot"),
        ("expected_timeline", "Soon"),
        ("project_stage", "Unknown"),
    ],
)
def test_inquiry_rejects_unsupported_planning_values(valid_payload, field, value):
    valid_payload[field] = value

    with pytest.raises(ValidationError, match="Choose a supported"):
        InquiryCreate.model_validate(valid_payload)


def test_project_brief_uses_submitted_values(valid_payload):
    inquiry = InquiryCreate.model_validate(valid_payload)

    brief = generate_project_brief(inquiry)

    assert "Project: Support assistant" in brief
    assert "Category: AI & Automation" in brief
    assert "Functional scope: AI chatbot or virtual assistant" in brief
    assert "Budget: Below ₹25,000" in brief
    assert "Contact: Asha Test (asha@example.com)" in brief


def test_save_inquiry_requires_database_url(valid_payload, monkeypatch):
    inquiry = InquiryCreate.model_validate(valid_payload)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL is not configured"):
        save_inquiry(inquiry, uuid4(), generate_project_brief(inquiry))


class FakeCursor:
    def __init__(self, insert_result, existing_result):
        self.insert_result = insert_result
        self.existing_result = existing_result
        self.last_sql = ""
        self.last_params = None
        self.statements = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params=None):
        self.last_sql = sql
        self.last_params = params
        self.statements.append(sql)

    def fetchone(self):
        if "RETURNING id, created_at, project_brief" in self.last_sql:
            return self.insert_result
        if self.last_sql.lstrip().startswith("SELECT id, created_at, project_brief"):
            return self.existing_result
        return None


class FakeConnection:
    def __init__(self, cursor):
        self.fake_cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def cursor(self):
        return self.fake_cursor


@pytest.mark.parametrize("is_duplicate", [False, True])
def test_save_inquiry_returns_insert_or_idempotent_existing_row(
    valid_payload, monkeypatch, is_duplicate
):
    inquiry = InquiryCreate.model_validate(valid_payload)
    idempotency_key = uuid4()
    saved_id = uuid4()
    created_at = datetime(2026, 10, 31, 12, 0, tzinfo=timezone.utc)
    saved_brief = generate_project_brief(inquiry)
    inserted = None if is_duplicate else (saved_id, created_at, saved_brief)
    existing = (saved_id, created_at, saved_brief)
    cursor = FakeCursor(inserted, existing)
    monkeypatch.setenv("DATABASE_URL", "postgresql://test-only.invalid/database")
    monkeypatch.setattr(
        "app.services.inquiries.psycopg.connect",
        lambda _: FakeConnection(cursor),
    )

    result = save_inquiry(inquiry, idempotency_key, saved_brief)

    assert result["id"] == str(saved_id)
    assert result["reference_id"] == str(saved_id)
    assert result["project_brief"] == saved_brief
    assert "ON CONFLICT (idempotency_key) DO NOTHING" in cursor.statements[1]
    if is_duplicate:
        assert cursor.statements[2].lstrip().startswith("SELECT id, created_at")
        assert cursor.last_params == (idempotency_key,)
