import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routes import router

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("FitBuddy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event to auto-create tables on startup."""
    logger.info("Initializing FitBuddy SQLite database tables...")
    init_db()
    logger.info("FitBuddy ready to accept requests.")
    yield
    logger.info("FitBuddy shutting down.")


# FastAPI Application Instance (This is what Uvicorn looks for)
app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="Personalized 7-day workout and nutrition plan generator powered by Google Gemini Models.",
    version="1.0.0",
    lifespan=lifespan
)

# Static Files Setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure static directory exists
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "images"), exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Register Routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)