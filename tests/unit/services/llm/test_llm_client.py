from unittest.mock import patch, MagicMock

from app.services.llm.llm_client import (
    infer_experiences_from_prompt,
    filter_relevant_news_from_prompt,
    call_openai_chat,
)


# --- infer_experiences_from_prompt 테스트 ---
@patch("app.services.llm.llm_client.call_openai_chat")
def test_infer_experiences_from_prompt_returns_list(mock_call):
    mock_call.return_value = ["대기업 경험", "리더쉽"]
    prompt = "테스트용 프롬프트"

    result = infer_experiences_from_prompt(prompt)

    assert isinstance(result, list)
    assert "대기업 경험" in result
    mock_call.assert_called_once()


# --- filter_relevant_news_from_prompt 테스트 ---
@patch("app.services.llm.llm_client.call_openai_chat")
def test_filter_relevant_news_from_prompt_returns_filtered_list(mock_call):
    mock_call.return_value = ["카카오, AI 투자", "카카오, 블록체인 진출"]
    prompt = "뉴스 필터링 프롬프트"

    result = filter_relevant_news_from_prompt(prompt)

    assert isinstance(result, list)
    assert len(result) == 2
    mock_call.assert_called_once()


# --- call_openai_chat 테스트 ---
@patch("app.services.llm.llm_client.OpenAI")  # OpenAI 클래스를 patch
def test_call_openai_chat_parses_list_output(mock_openai_cls):
    # OpenAI 인스턴스 mocking
    mock_instance = MagicMock()
    mock_openai_cls.return_value = mock_instance
    # chat.completions.create() mocking
    mock_instance.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="- 경험 A\n- 경험 B\n- 경험 C"))
    ]

    result = call_openai_chat(
        system_prompt="시스템 프롬프트",
        user_prompt="유저 프롬프트",
        parse_mode="list"
    )

    assert result == ["경험 A", "경험 B", "경험 C"]



@patch("app.services.llm.llm_client.OpenAI")
def test_call_openai_chat_handles_exception_and_returns_empty(mock_openai_cls):
    # OpenAI 인스턴스를 흉내냄
    mock_instance = MagicMock()
    # create() 호출 시 예외 발생하도록 설정
    mock_instance.chat.completions.create.side_effect = Exception("API 실패")
    mock_openai_cls.return_value = mock_instance

    result = call_openai_chat(
        system_prompt="system",
        user_prompt="user",
        parse_mode="list"
    )

    # 리스트 모드니까 실패 시 빈 리스트 반환 확인
    assert result == []