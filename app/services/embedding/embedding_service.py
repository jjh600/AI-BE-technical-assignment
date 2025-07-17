from app.config import OPENAI_API_KEY
import openai
import logging
from typing import List

openai.api_key = OPENAI_API_KEY
logger = logging.getLogger(__name__)

def generate_embedding(text: str, model: str) -> List[float]:
    """
    단일 텍스트에 대해 OpenAI 임베딩을 생성합니다.
    """
    logger.debug(f"[임베딩 요청] 단일 텍스트 길이: {len(text)}")
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def generate_embeddings_batch(texts: List[str], model: str) -> List[List[float]]:
    """
    다수의 텍스트에 대해 OpenAI 임베딩을 일괄 생성합니다.
    """
    logger.debug(f"[임베딩 요청] 배치 크기: {len(texts)}")
    response = openai.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]
