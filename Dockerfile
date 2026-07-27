# Base image: official, slim Python 3.12. "slim" = fewer OS packages = smaller,
# more secure image. Same principle as choosing a minimal base VM image.
FROM python:3.12-slim

# All following commands run from /app inside the container.
WORKDIR /app

# Copy ONLY requirements.txt first (not the whole app yet).
# Why: Docker caches each instruction as a "layer". If we copied all the code
# first, changing one line of Python would force a full reinstall of every
# dependency on every rebuild. By copying requirements.txt first, Docker only
# re-runs "pip install" when requirements.txt itself changes.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual application code.
COPY app ./app

# Documents that the container listens on port 8000 (informational — doesn't
# actually publish the port, docker-compose.yml does that).
EXPOSE 8000

# The command that runs when the container starts.
# --host 0.0.0.0 means "listen on all network interfaces" (required so the
# port can be reached from outside the container).
# --reload watches for code changes and restarts automatically — dev only,
# we will remove this for production images later.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
