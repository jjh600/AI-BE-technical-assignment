from app.config import OPENAI_API_KEY
import openai
import logging
from typing import List


openai.api_key = OPENAI_API_KEY
logger = logging.getLogger(__name__)


def generate_embedding(text: str, model: str) -> list[float]:
    logger.info(f"Generating embedding for {text}")
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def generate_embeddings_batch(texts: List[str], model: str):
    response = openai.embeddings.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]
