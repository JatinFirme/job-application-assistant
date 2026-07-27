from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.job import Job
from app.services.adzuna_client import AdzunaClient

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/fetch")
def fetch_jobs(
    country: str = Query(..., description="Two-letter country code, e.g. us, in, sg, gb, au, ca"),
    what: str = Query(..., description="Search keywords, e.g. 'site reliability engineer'"),
    db: Session = Depends(get_db),
):
    """
    Calls Adzuna, then inserts any NEW jobs into our database.
    Jobs we already have (matched by source + source_job_id) are skipped --
    this is what the unique constraint from Module 3A protects us from.
    """
    client = AdzunaClient()
    normalized_jobs = client.search(country=country, what=what)

    inserted = 0
    skipped = 0

    for job_data in normalized_jobs:
        exists = db.scalar(
            select(Job).where(
                Job.source == job_data["source"],
                Job.source_job_id == job_data["source_job_id"],
            )
        )
        if exists:
            skipped += 1
            continue

        db.add(Job(**job_data))
        inserted += 1

    db.commit()

    return {"fetched": len(normalized_jobs), "inserted": inserted, "skipped": skipped}


@router.get("/")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.scalars(select(Job)).all()
    return [
        {
            "id": j.id,
            "source": j.source,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "country": j.country,
            "salary_min": j.salary_min,
            "salary_max": j.salary_max,
            "url": j.url,
            "posted_at": j.posted_at,
        }
        for j in jobs
    ]
