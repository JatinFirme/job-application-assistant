from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Resume(Base):
    """
    Represents one row in the "resumes" table. Each attribute below becomes
    a column. This class is the ONLY place that defines the resume table's
    shape -- every other part of the app imports this class instead of
    writing raw SQL column names, so a typo gets caught by Python itself
    instead of failing silently at query time.
    """

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(String(500))
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
