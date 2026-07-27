from datetime import datetime, timezone

from sqlalchemy import String, Text, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Job(Base):
    """
    A normalized job posting, regardless of which external source it came
    from. Every source-specific fetcher (Adzuna today, others later) is
    responsible for translating its own raw response into this shape.
    """

    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("source", "source_job_id", name="uq_source_job"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(50))
    source_job_id: Mapped[str] = mapped_column(String(100))

    title: Mapped[str] = mapped_column(String(300))
    company: Mapped[str] = mapped_column(String(300))
    location: Mapped[str] = mapped_column(String(300))
    country: Mapped[str] = mapped_column(String(10))

    description: Mapped[str] = mapped_column(Text)

    salary_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    url: Mapped[str] = mapped_column(String(1000))

    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
