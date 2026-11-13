from fastapi import FastAPI

app = FastAPI(
    title="PSI API",
    version="0.1.0",
    description="Personal Storage Infrastructure API",
)


@app.get("/api/v1/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "psi-api"}
