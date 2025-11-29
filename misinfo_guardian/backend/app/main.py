import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.verify import router as verify_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("misinfo_guardian")

app = FastAPI(title="Misinformation Guardian Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow extension calls during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    logger.info("Health check ping received")
    return {
        "status": "ok",
        "version": "1.0.0",
        "service": "misinformation_guardian_backend"
    }

app.include_router(verify_router, prefix="/api")
