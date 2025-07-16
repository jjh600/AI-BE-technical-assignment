from app.utils.position_utils import (
    parse_position_dates,
    normalize_position_description,
    build_embedding_text
)
from types import SimpleNamespace

def test_parse_position_dates():
    position = SimpleNamespace(
        startEndDate=SimpleNamespace(
            start=SimpleNamespace(year=2020, month=1),
            end=SimpleNamespace(year=2021, month=12)
        )
    )
    start, end = parse_position_dates(position)
    assert start == "2020-01-01"
    assert end == "2021-12-31"

def test_normalize_position_description():
    assert normalize_position_description("개발\n운영") == "개발, 운영"
    assert normalize_position_description(None) == "설명 없음"

def test_build_embedding_text():
    position = SimpleNamespace(
        companyName="OpenAI",
        title="Researcher",
        description="LLM 연구\n성능 테스트",
        startEndDate=SimpleNamespace(
            start=SimpleNamespace(year=2020),
            end=SimpleNamespace(year=2022)
        )
    )
    text = build_embedding_text(position)
    assert "회사명: OpenAI" in text
    assert "직무: Researcher" in text
    assert "설명: LLM 연구 성능 테스트" in text
    assert "기간: 2020–2022" in text
