import os


class Settings:
    """
    Centralizes all environment-based configuration in one place.

    This is a Clean Architecture principle: configuration is an
    "infrastructure" concern. Nothing else in the app should know or care
    HOW config is loaded (env var today, maybe Azure Key Vault or AWS
    Secrets Manager later) -- it just reads `settings.database_url`.
    """

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/job_assistant",
    )


settings = Settings()
