from fastapi import FastAPI
from app.api.v1.inference import router as rag_router
from app.utils.logger import setup_logger

setup_logger()
app = FastAPI()
app.include_router(rag_router, prefix="/api/v1/inference", tags=["Inference"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
