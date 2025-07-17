from typing import List, Literal
from openai import OpenAI

import logging

from app.constants import DEFAULT_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS
from app.services.llm.templates import TEMPLATE_SYSTEM_PROMPT_EXPERIENCE, TEMPLATE_SYSTEM_PROMPT_NEWS_FILTER

logger = logging.getLogger(__name__)


def call_openai_chat(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = MAX_TOKENS,
    parse_mode: Literal["list", "json", "raw"] = "list",
    top_p: float = None,
) -> List[str] | dict | str:
    """
    OpenAI ChatCompletion 호출 래퍼 함수

    Args:
        system_prompt (str): 시스템 메시지
        user_prompt (str): 사용자 입력 메시지
        model (str): 사용할 OpenAI 모델 이름
        parse_mode (str): 출력 포맷 ('list', 'json', 'raw')

    Returns:
        List[str] | dict | str: LLM 응답 파싱 결과
    """

    client = OpenAI()

    try:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("시스템 프롬프트:\n" + system_prompt)
            logger.debug("유저 프롬프트:\n" + user_prompt)

        kwargs = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "n": 1,
        }
        if top_p is not None:
            kwargs["top_p"] = top_p

        response = client.chat.completions.create(**kwargs)
        output = response.choices[0].message.content.strip()
        logger.debug("LLM 수행 결과: \n" + output)

        if parse_mode == "json":
            import json
            return json.loads(output)

        elif parse_mode == "list":

            return [
                line.strip("-•0123456789. ").strip()
                for line in output.split("\n")
                if line.strip()
            ]

        return output  # parse_mode == "raw"

    except Exception as e:
        logger.error(f"OpenAI 호출 실패: {e}\nPrompt: {user_prompt[:200]}")
        return [] if parse_mode in ["list", "json"] else ""


def infer_experiences_from_prompt(prompt: str) -> List[str]:
    return call_openai_chat(TEMPLATE_SYSTEM_PROMPT_EXPERIENCE, prompt, parse_mode="list")

def filter_relevant_news_from_prompt(prompt: str) -> List[str]:
    return call_openai_chat(TEMPLATE_SYSTEM_PROMPT_NEWS_FILTER, prompt, parse_mode="list", temperature=0, top_p=0.1)
