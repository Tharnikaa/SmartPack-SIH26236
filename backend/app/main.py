import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import router as api_router
from app.services.data_service import data_service
from app.ml.train import model_trainer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SmartPack")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing SmartPack Recommendation Backend...")
    # Verify datasets loaded
    data_service.load_all_datasets()
    # Check if ML model exists, if not trigger initial training
    model_file = "models/packaging_suitability_model.pkl"
    if not os.path.exists(model_file):
        logger.info("No pre-existing ML model bundle found; running initial training...")
        model_trainer.train_model()
    else:
        logger.info("Pre-existing ML model bundle found and ready.")
    yield
    logger.info("Shutting down SmartPack backend.")

app = FastAPI(
    title="SmartPack - AI-Assisted Food Packaging Recommendation System",
    description="SIH Problem Statement 26236: Scientific Hybrid Food-Packaging Recommendation API",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to SmartPack Recommendation Engine API",
        "docs_url": "/docs",
        "api_prefix": "/api"
    }
