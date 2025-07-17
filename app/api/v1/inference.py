from fastapi import APIRouter, HTTPException
import logging

from app.core.rag_pipeline import run_experience_pipeline
from app.schemas.inference import ExperienceInferenceInput, ExperienceInferenceOutput

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/experience", response_model=ExperienceInferenceOutput, summary="LLM 기반 경험 태그 추론")
async def infer_experience(data: ExperienceInferenceInput):
    try:
        return run_experience_pipeline(data)
    except Exception as e:
        logger.error(f"[RAG 실패] {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"RAG failed: {str(e)}")
