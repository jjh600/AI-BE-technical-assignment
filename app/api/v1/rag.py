from fastapi import APIRouter, HTTPException

from app.core.rag_pipeline import process_inference_pipeline
from app.schemas.rag import InferenceInput, InferenceOutput

router = APIRouter()

@router.post("", response_model=InferenceOutput, summary="LLM 기반 경험 추론")
async def run_rag(data: InferenceInput):
    try:
        return process_inference_pipeline(data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG failed: {str(e)}")
