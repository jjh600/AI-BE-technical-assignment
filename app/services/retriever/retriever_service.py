from typing import List

from app.config import EMBEDDING_MODEL
from app.db.vector_store import retrieve_similar_rows
from app.services.embedding.embedding_service import generate_embedding
from app.utils.position_utils import parse_position_dates, build_embedding_text

import logging

logger = logging.getLogger(__name__)

def generate_position_query_embedding(position, model: str = EMBEDDING_MODEL):
    embedding_text = build_embedding_text(position)
    embedding = generate_embedding(embedding_text, model)
    logger.debug(f"[임베딩 생성] text: {embedding_text}, len: {len(embedding)}")

    return embedding

def get_news_filters(position, company_map) -> dict:
    start_date, end_date = parse_position_dates(position)
    filters = {
        "news_date >=": start_date,
        "news_date <=": end_date,
    }
    cid = company_map.get(position.companyName)
    if cid:
        filters["company_id"] = cid

    return filters

def retrieve_news_for_position(position, company_map) -> List[str]:
    query_embedding = generate_position_query_embedding(position)
    filters = get_news_filters(position, company_map)

    similar_news = retrieve_similar_rows(
        table="company_news",
        embedding_column="embedding",
        query_embedding=query_embedding,
        filters=filters
    )

    return [row[1] for row in similar_news]
