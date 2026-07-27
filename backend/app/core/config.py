import os


class Settings:
    """
    Centralizes all environment-based configuration in one place.
    """

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/job_assistant",
    )

    upload_dir: str = os.getenv("UPLOAD_DIR", "/app/uploads")

    # Adzuna credentials -- loaded from backend/.env, never committed to Git.
    adzuna_app_id: str = os.getenv("ADZUNA_APP_ID", "")
    adzuna_app_key: str = os.getenv("ADZUNA_APP_KEY", "")


settings = Settings()
