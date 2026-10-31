from app.data.project_options import CATEGORY_LABELS
from app.schemas.inquiry import InquiryCreate


def generate_project_brief(inquiry: InquiryCreate) -> str:
    requirements = list(inquiry.requirements)
    if inquiry.other_requirement:
        requirements.append(inquiry.other_requirement)

    project_name = inquiry.project_title or CATEGORY_LABELS[inquiry.project_category]
    contact = inquiry.full_name
    if inquiry.email:
        contact = f"{contact} ({inquiry.email})"

    return "\n".join(
        [
            f"Project: {project_name}",
            f"Category: {CATEGORY_LABELS[inquiry.project_category]}",
            f"Problem: {inquiry.problem_statement}",
            f"Objective: {inquiry.objective}",
            f"Functional scope: {'; '.join(requirements)}",
            f"Budget: {inquiry.budget_range}",
            f"Timeline: {inquiry.expected_timeline}",
            f"Project stage: {inquiry.project_stage}",
            f"Contact: {contact}",
        ]
    )
