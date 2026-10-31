import json
import os
from uuid import UUID, uuid4

import psycopg

from app.schemas.inquiry import InquiryCreate


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS inquiries (
    id UUID PRIMARY KEY,
    idempotency_key UUID NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    company_name VARCHAR(120),
    phone_number VARCHAR(30),
    project_category VARCHAR(40) NOT NULL,
    project_title VARCHAR(120),
    problem_statement TEXT NOT NULL,
    objective VARCHAR(600) NOT NULL,
    requirements JSONB NOT NULL DEFAULT '[]'::jsonb,
    other_requirement VARCHAR(300),
    budget_range VARCHAR(40) NOT NULL,
    expected_timeline VARCHAR(40) NOT NULL,
    project_stage VARCHAR(60) NOT NULL,
    project_brief TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
"""


def save_inquiry(inquiry: InquiryCreate, idempotency_key: UUID, project_brief: str) -> dict:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    inquiry_id = uuid4()
    insert_sql = """
    INSERT INTO inquiries (
        id, idempotency_key, full_name, email, company_name, phone_number,
        project_category, project_title, problem_statement, objective,
        requirements, other_requirement, budget_range, expected_timeline,
        project_stage, project_brief
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s::jsonb, %s, %s, %s, %s, %s
    )
    ON CONFLICT (idempotency_key) DO NOTHING
    RETURNING id, created_at, project_brief
    """

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
            cursor.execute(
                insert_sql,
                (
                    inquiry_id,
                    idempotency_key,
                    inquiry.full_name,
                    str(inquiry.email),
                    inquiry.company_name,
                    inquiry.phone_number,
                    inquiry.project_category,
                    inquiry.project_title,
                    inquiry.problem_statement,
                    inquiry.objective,
                    json.dumps(inquiry.requirements),
                    inquiry.other_requirement,
                    inquiry.budget_range,
                    inquiry.expected_timeline,
                    inquiry.project_stage,
                    project_brief,
                ),
            )
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    "SELECT id, created_at, project_brief FROM inquiries WHERE idempotency_key = %s",
                    (idempotency_key,),
                )
                result = cursor.fetchone()

    if result is None:
        raise RuntimeError("The inquiry could not be saved.")

    saved_id, created_at, saved_brief = result
    return {
        "id": str(saved_id),
        "reference_id": str(saved_id),
        "created_at": created_at.isoformat(),
        "project_brief": saved_brief,
    }
