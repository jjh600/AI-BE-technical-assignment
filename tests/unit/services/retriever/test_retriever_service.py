import pytest
from unittest.mock import patch

from app.db.vector_store import build_similarity_query_parts
from app.services.retriever.retriever_service import get_news_filters, retrieve_news_for_position

from app.schemas.rag import Position, StartEndDate, PositionDate

def test_cosine_metric_query_parts():
    col = "embedding"
    similarity, where = build_similarity_query_parts(col, metric="cosine")

    assert "1 - (embedding <=>" in similarity
    assert "1 - (embedding <=>" in where
    assert ">= %s" in where

def test_inner_product_query_parts():
    col = "embedding"
    similarity, where = build_similarity_query_parts(col, metric="inner_product")

    assert "<#>" in similarity
    assert "embedding" in similarity
    assert ">= %s" in where

def test_invalid_metric_raises():
    col = "embedding"
    with pytest.raises(ValueError) as exc_info:
        build_similarity_query_parts(col, metric="manhattan")

    assert "Unsupported metric" in str(exc_info.value)

def test_get_news_filters_with_company_id():
    position = Position(
        companyName="네이버",
        title="백엔드 엔지니어",
        startEndDate=StartEndDate(
            start=PositionDate(year=2021, month=1),
            end=PositionDate(year=2022, month=12)
        ),
        description="test",
        companyLocation="서울"
    )

    company_map = {"네이버": 2}

    filters = get_news_filters(position, company_map)

    assert filters["news_date >="] == "2021-01-01"
    assert filters["news_date <="] == "2022-12-31"
    assert filters["company_id"] == 2

def test_get_news_filters_without_company_id():
    position = Position(
        companyName="없는회사",
        title="직무",
        startEndDate=StartEndDate(
            start=PositionDate(year=2020, month=5),
            end=PositionDate(year=2021, month=1)
        ),
        description="test",
        companyLocation="서울"
    )
    company_map = {"네이버": 2}

    filters = get_news_filters(position, company_map)

    assert "company_id" not in filters
    assert filters["news_date >="] == "2020-05-01"
    assert filters["news_date <="] == "2021-01-31"

@patch("app.services.retriever.retriever_service.retrieve_similar_rows")
@patch("app.services.retriever.retriever_service.get_news_filters")
@patch("app.services.retriever.retriever_service.generate_position_query_embedding")
def test_retrieve_news_for_position(mock_embed, mock_filters, mock_similar_rows):
    # Mock 값 세팅
    mock_embed.return_value = [0.1] * 1536
    mock_filters.return_value = {
        "company_id": 1,
        "news_date >=": "2022-01-01",
        "news_date <=": "2023-01-01"
    }
    mock_similar_rows.return_value = [
        (1, "카카오, AI 사업 강화", 0.92),
        (2, "카카오, 블록체인 진출", 0.89)
    ]

    # 테스트 입력
    position = Position(
        companyName="카카오",
        title="AI 엔지니어",
        startEndDate=StartEndDate(
            start=PositionDate(year=2022, month=1),
            end=PositionDate(year=2023, month=1)
        ),
        description="AI 기반 추천 시스템 개발",
        companyLocation="판교"
    )
    company_map = {"카카오": 1}

    # 실행
    result = retrieve_news_for_position(position, company_map)

    # 검증
    assert result == ["카카오, AI 사업 강화", "카카오, 블록체인 진출"]
    mock_embed.assert_called_once_with(position)
    mock_filters.assert_called_once_with(position, company_map)
    mock_similar_rows.assert_called_once()
