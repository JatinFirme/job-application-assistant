from datetime import datetime

import httpx

from app.core.config import settings

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"


class AdzunaClient:
    """
    The ONLY piece of code in this app that knows Adzuna's specific API
    shape. Its job is to fetch raw results and translate each one into
    our own normalized dict shape (matching the Job model's columns).
    Nothing downstream of this class should ever see raw Adzuna JSON.
    """

    def __init__(self):
        self.app_id = settings.adzuna_app_id
        self.app_key = settings.adzuna_app_key

    def search(self, country: str, what: str, page: int = 1) -> list[dict]:
        """
        country: Adzuna's two-letter country code, e.g. "us", "in", "sg"
        what: search keywords, e.g. "site reliability engineer"
        """
        url = f"{ADZUNA_BASE_URL}/{country}/search/{page}"
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": what,
            "results_per_page": 20,
            "content-type": "application/json",
        }

        response = httpx.get(url, params=params, timeout=10.0)
        response.raise_for_status()  # raises an exception on 4xx/5xx responses
        data = response.json()

        return [self._normalize(raw, country) for raw in data.get("results", [])]

    def _normalize(self, raw: dict, country: str) -> dict:
        """
        Translates one raw Adzuna job dict into our normalized Job shape.
        This is the mapping layer -- when we add a second source later,
        THIS is the method that gets rewritten for that source's fields.
        """
        salary_min = raw.get("salary_min")
        salary_max = raw.get("salary_max")

        posted_at = None
        if raw.get("created"):
            # Adzuna returns ISO-8601 timestamps, e.g. "2026-07-20T10:00:00Z"
            posted_at = datetime.fromisoformat(raw["created"].replace("Z", "+00:00"))

        return {
            "source": "adzuna",
            "source_job_id": str(raw["id"]),
            "title": raw.get("title", ""),
            "company": raw.get("company", {}).get("display_name", "Unknown"),
            "location": raw.get("location", {}).get("display_name", ""),
            "country": country,
            "description": raw.get("description", ""),
            "salary_min": int(salary_min) if salary_min else None,
            "salary_max": int(salary_max) if salary_max else None,
            "url": raw.get("redirect_url", ""),
            "posted_at": posted_at,
        }
