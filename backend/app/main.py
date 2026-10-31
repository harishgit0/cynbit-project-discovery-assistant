import os
import logging
from uuid import UUID

import psycopg
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.inquiry import InquiryCreate, InquiryCreated
from app.services.briefs import generate_project_brief
from app.services.inquiries import save_inquiry


logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cynbit Project Discovery API",
    version="0.1.0",
    description="API for the Cynbit website improvement prototype.",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Idempotency-Key"],
)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "cynbit-discovery-api"}


@app.post("/api/inquiries", response_model=InquiryCreated, status_code=201)
def create_inquiry(
    inquiry: InquiryCreate,
    idempotency_key: UUID = Header(alias="Idempotency-Key"),
) -> InquiryCreated:
    project_brief = generate_project_brief(inquiry)
    try:
        return save_inquiry(inquiry, idempotency_key, project_brief)
    except (RuntimeError, psycopg.Error) as error:
        logger.exception("Could not persist project inquiry")
        raise HTTPException(
            status_code=503,
            detail="Inquiry storage is not available right now. Your details have not been submitted; please try again shortly.",
        ) from error
