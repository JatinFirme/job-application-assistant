# Job Application Assistant

AI-powered job search, ranking, tracking, and cover-letter assistant.
The user always manually reviews and submits applications — this tool
never auto-applies.

## Status
Module 0: dev environment + "hello world" backend container.

## Project structure
```
job-application-assistant/
├── backend/
│   ├── app/
│   │   └── main.py        # FastAPI app (routes live here)
│   ├── Dockerfile          # How to build the backend image
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml       # How to run the backend container
├── Makefile                 # Shortcut commands (make up, make down, ...)
└── .gitignore
```

## Run it locally

```bash
make build   # builds the Docker image
make up      # starts the container, logs stream to your terminal
```

Then open http://localhost:8000 in a browser — you should see:
```json
{"status": "ok", "message": "Job Application Assistant API is running"}
```

Also check http://localhost:8000/docs — FastAPI auto-generates interactive
API documentation for every endpoint you write. This will become very
useful as we add more routes.

Stop the container with `Ctrl+C`, then `make down` to clean up.
