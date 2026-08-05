from fastapi import FastAPI

app = FastAPI(
    title="AI Personal Finance API",
    description="Backend API for the AI Personal Finance Intelligence System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Personal Finance API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }