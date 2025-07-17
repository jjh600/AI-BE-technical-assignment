from typing import List
import logging

from app.config import EMBEDDING_MODEL
from app.constants import NEWS_TABLE, EMBEDDING_COLUMN
from app.db.vector_store import retrieve_similar_rows
from app.services.embedding.embedding_service import generate_embedding
from app.utils.position_utils import parse_position_dates, build_embedding_text
from app.schemas.inference import Position

logger = logging.getLogger(__name__)


def generate_position_query_embedding(position: Position, model: str = EMBEDDING_MODEL) -> List[float]:
    """
    포지션 정보를 기반으로 검색용 임베딩 벡터 생성
    """
    embedding_text = build_embedding_text(position)
    embedding = generate_embedding(embedding_text, model)
    logger.debug(f"[임베딩 생성] text: {embedding_text}, result_len: {len(embedding)}")
    return embedding

def build_news_filters(position: Position, company_map: dict[str, int]) -> dict:
    """
    재직 기간 및 기업 ID에 따른 뉴스 필터 조건 생성
    """
    start_date, end_date = parse_position_dates(position)
    filters = {
        "news_date >=": start_date,
        "news_date <=": end_date,
    }
    cid = company_map.get(position.companyName)
    if cid:
        filters["company_id"] = cid
    return filters

def retrieve_news_for_position(position: Position, company_map: dict[str, int]) -> List[str]:
    """
    임베딩 기반 유사도 검색을 통해 해당 포지션과 관련된 뉴스 제목 리스트 반환
    """
    query_embedding = generate_position_query_embedding(position)
    filters = build_news_filters(position, company_map)

    similar_news = retrieve_similar_rows(
        table=NEWS_TABLE,
        embedding_column=EMBEDDING_COLUMN,
        query_embedding=query_embedding,
        filters=filters
    )

    return [row[1] for row in similar_news]  # 뉴스 제목만 반환
