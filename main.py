from fastapi import FastAPI

# This creates the FastAPI "application" object.
# Think of this as the equivalent of starting an nginx/HAProxy instance —
# every route we add below gets attached to this one object.
app = FastAPI(title="Job Application Assistant API")


@app.get("/")
def read_root():
    """
    This function runs whenever someone sends an HTTP GET request to "/".
    FastAPI turns the returned Python dict into a JSON response automatically.
    """
    return {"status": "ok", "message": "Job Application Assistant API is running"}


@app.get("/health")
def health_check():
    """
    A dedicated health check endpoint. You already use these for Kubernetes
    liveness/readiness probes and Azure Monitor — same idea, we're just
    building the endpoint it calls.
    """
    return {"status": "healthy"}
