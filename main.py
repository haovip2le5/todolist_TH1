from fastapi import FastAPI

app = FastAPI(title="Todo API")


@app.get("/health")
def health():
    """Kiểm tra sức khỏe API"""
    return {"status": "ok"}


@app.get("/")
def root():
    """Endpoint chào mừng"""
    return {"message": "Chào mừng đến Todo API"}
