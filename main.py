from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.models import todo  # Import models to register them
from app.routers import todo as todo_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)


# ===== Health =====
@app.get("/health")
def health():
    """Kiểm tra sức khỏe API"""
    return {"status": "ok", "app": settings.APP_NAME}


# ===== Root =====
@app.get("/")
def root():
    """Endpoint chào mừng"""
    return {
        "message": f"Chào mừng đến {settings.APP_NAME}",
        "version": settings.VERSION
    }


# ===== Include routers =====
app.include_router(todo_router.router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
