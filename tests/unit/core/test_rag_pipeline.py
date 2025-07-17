import pytest
from unittest.mock import patch

from app.core.rag_pipeline import (
    filter_news_for_position,
    run_experience_pipeline,
)
from app.schemas.inference import (
    ExperienceInferenceInput,
    Position,
    StartEndDate,
    PositionDate,
)

@patch("app.core.rag_pipeline.filter_relevant_news_from_prompt")
@patch("app.core.rag_pipeline.build_news_filter_prompt")
@patch("app.core.rag_pipeline.retrieve_news_for_position")
def test_filter_news_for_position_returns_filtered_news(
    mock_retrieve_news, mock_build_prompt, mock_filter_news
):
    # 1. Mock 세팅
    mock_retrieve_news.return_value = ["카카오, AI 투자", "카카오, 블록체인 진출"]
    mock_build_prompt.return_value = "뉴스 필터 프롬프트"
    mock_filter_news.return_value = ["카카오, AI 투자"]

    # 2. 입력값 구성
    position = Position(
        companyName="카카오",
        title="AI 엔지니어",
        startEndDate=StartEndDate(
            start=PositionDate(year=2022, month=1),
            end=PositionDate(year=2023, month=1)
        ),
        description="AI 관련 백엔드 개발",
        companyLocation="판교"
    )
    company_map = {"카카오": 1}

    # 3. 실행
    result = filter_news_for_position(position, company_map)

    # 4. 검증
    assert result == ["카카오, AI 투자"]
    mock_retrieve_news.assert_called_once_with(position, company_map)
    mock_build_prompt.assert_called_once_with(position, mock_retrieve_news.return_value)
    mock_filter_news.assert_called_once_with("뉴스 필터 프롬프트")

@patch("app.core.rag_pipeline.run_experience_inference")
@patch("app.core.rag_pipeline.build_experience_tag_prompt")
@patch("app.core.rag_pipeline.prepare_all_filtered_news")
def test_process_inference_pipeline_returns_output(
    mock_prepare_news, mock_generate_prompt, mock_run_inference
):
    # 1. Mock 설정
    mock_prepare_news.return_value = [["뉴스 A", "뉴스 B"]]
    mock_generate_prompt.return_value = "프롬프트 본문"
    mock_run_inference.return_value = ["대기업 경험", "리더십"]

    # 2. 입력값 생성
    input_data = ExperienceInferenceInput(
        firstName="지훈",
        lastName="박",
        positions=[
            Position(
                title="프론트엔드 개발자",
                companyName="네이버",
                startEndDate=StartEndDate(
                    start=PositionDate(year=2020, month=5),
                    end=PositionDate(year=2022, month=7)
                ),
                description="웹 UI 개발",
                companyLocation="분당"
            )
        ]
    )

    # 3. 실행
    result = run_experience_pipeline(input_data)

    # 4. 검증
    assert result.experiences == ["대기업 경험", "리더십"]
    mock_prepare_news.assert_called_once_with(input_data)
    mock_generate_prompt.assert_called_once_with(input_data, [["뉴스 A", "뉴스 B"]])
    mock_run_inference.assert_called_once_with("프롬프트 본문")
