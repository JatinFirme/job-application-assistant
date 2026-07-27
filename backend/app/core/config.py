import os


class Settings:
    """
    Centralizes all environment-based configuration in one place.
    """

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/job_assistant",
    )

    # Where uploaded resume files get saved inside the container. Because
    # docker-compose.yml mounts ./backend to /app, anything written here
    # also appears on your host at backend/uploads/.
    upload_dir: str = os.getenv("UPLOAD_DIR", "/app/uploads")


settings = Settings()
