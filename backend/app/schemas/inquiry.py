from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.data.project_options import (
    BUDGET_OPTIONS,
    REQUIREMENTS_BY_CATEGORY,
    STAGE_OPTIONS,
    TIMELINE_OPTIONS,
)


ProjectCategory = Literal[
    "ai_automation",
    "web_mobile",
    "saas_platform",
    "backend_cloud",
    "digital_marketing_crm",
    "other_custom",
]


class InquiryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    company_name: str | None = Field(default=None, max_length=120)
    phone_number: str | None = Field(default=None, max_length=30)
    project_category: ProjectCategory
    project_title: str | None = Field(default=None, max_length=120)
    problem_statement: str = Field(min_length=20, max_length=2000)
    objective: str = Field(min_length=10, max_length=600)
    requirements: list[str] = Field(default_factory=list, max_length=20)
    other_requirement: str | None = Field(default=None, max_length=300)
    budget_range: str
    expected_timeline: str
    project_stage: str

    @model_validator(mode="after")
    def validate_options_and_scope(self):
        if self.budget_range not in BUDGET_OPTIONS:
            raise ValueError("Choose a supported budget range.")
        if self.expected_timeline not in TIMELINE_OPTIONS:
            raise ValueError("Choose a supported timeline.")
        if self.project_stage not in STAGE_OPTIONS:
            raise ValueError("Choose a supported project stage.")

        supported = REQUIREMENTS_BY_CATEGORY[self.project_category]
        if len(self.requirements) != len(set(self.requirements)):
            raise ValueError("A requirement can only be selected once.")
        if any(requirement not in supported for requirement in self.requirements):
            raise ValueError("One or more requirements are not available for this category.")
        if not self.requirements and not (self.other_requirement or "").strip():
            raise ValueError("Select at least one requirement or describe another one.")
        return self


class InquiryCreated(BaseModel):
    id: str
    reference_id: str
    created_at: str
    project_brief: str
