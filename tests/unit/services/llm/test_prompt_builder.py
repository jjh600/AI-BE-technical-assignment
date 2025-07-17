from app.schemas.inference import ExperienceInferenceInput, Position, StartEndDate, PositionDate
from app.services.llm.prompt_builder import (
    build_experience_tag_prompt,
    build_news_filter_prompt,
)


def test_build_experience_tag_prompt_minimal():
    input_data = ExperienceInferenceInput(
        firstName="지훈",
        lastName="박",
        summary="테스트 요약",
        skills=["Python"],
        positions=[
            Position(
                title="백엔드 개발자",
                companyName="카카오",
                startEndDate=StartEndDate(
                    start=PositionDate(year=2021, month=1),
                    end=PositionDate(year=2022, month=1)
                ),
                description="서버 개발",
                companyLocation="판교"
            )
        ],
        educations=[],
    )

    news = [["카카오, 백엔드 개발자 대규모 채용"]]

    prompt = build_experience_tag_prompt(input_data, news)

    assert "카카오" in prompt
    assert "서버 개발" in prompt
    assert "백엔드 개발자" in prompt
    assert "테스트 요약" in prompt
    assert "Python" in prompt
    assert "경험 키워드" in prompt

def test_build_news_filter_prompt_structure():
    position = Position(
        title="프론트엔드 엔지니어",
        companyName="네이버",
        startEndDate=StartEndDate(
            start=PositionDate(year=2020, month=5),
            end=PositionDate(year=2022, month=6)
        ),
        description="UI 개발",
        companyLocation="서울"
    )
    news_list = [
        "네이버, 개발자 채용 확대",
        "네이버, 2021년 3분기 실적 발표"
    ]

    prompt = build_news_filter_prompt(position, news_list)

    assert "네이버" in prompt
    assert "프론트엔드 엔지니어" in prompt
    assert "- 네이버, 개발자 채용 확대" in prompt
    assert "포지션 설명" in prompt
    assert "뉴스 제목 목록" in prompt
