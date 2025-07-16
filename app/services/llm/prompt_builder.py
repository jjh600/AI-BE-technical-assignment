from typing import List
from app.schemas.rag import InferenceInput
from app.utils.position_utils import normalize_position_description
from app.services.llm.templates import (
    TEMPLATE_TAG_INFERENCE_HEADER,
    TEMPLATE_TAG_INFERENCE_CONDITIONS,
    TEMPLATE_TAG_INFERENCE_TAGS,
    TEMPLATE_TAG_INFERENCE_FORMAT_EXAMPLE,
    TEMPLATE_NEWS_FILTER_CONDITIONS,
    TEMPLATE_NEWS_FILTER_EXAMPLE,
)

def generate_fixed_tags_prompt(input_data: InferenceInput, news_per_position: List[List[str]]) -> str:
    education_info = []
    for edu in input_data.educations or []:
        school = edu.schoolName or ""
        degree = edu.degreeName or ""
        major = edu.fieldOfStudy or ""
        if school:
            parts = [school]
            if degree:
                parts.append(f"({degree})")
            if major:
                parts.append(f"- {major}")
            education_info.append(" ".join(parts))
    education_text = ", ".join(education_info) if education_info else "없음"

    skills_text = ", ".join(input_data.skills) if input_data.skills else "없음"

    position_news_blocks = []
    for i, position in enumerate(input_data.positions):
        company = position.companyName or "회사명 미상"
        title = position.title or "직함 미상"
        desc = normalize_position_description(position.description)
        news_titles = news_per_position[i]
        news_lines = "\n".join([f"- {title}" for title in news_titles]) if news_titles else "- 해당 기간 관련 뉴스 없음"
        block = (
            f"[{company} / {title} 재직 시 이력 및 관련 뉴스]\n"
            f"포지션 설명: {desc}\n"
            f"{news_lines}"
        )
        position_news_blocks.append(block)

    prompt = f"""
{TEMPLATE_TAG_INFERENCE_HEADER}

{TEMPLATE_TAG_INFERENCE_CONDITIONS}

{TEMPLATE_TAG_INFERENCE_TAGS}

[인재 기본 정보]
- 한 줄 소개: {input_data.headline}
- 요약: {input_data.summary}
- 학력: {education_text}
- 보유 기술: {skills_text}

[포지션별 설명 및 관련 뉴스]
{chr(10).join(position_news_blocks)}

{TEMPLATE_TAG_INFERENCE_FORMAT_EXAMPLE}
""".strip()

    return prompt

def build_news_filter_prompt(position, news_list: List[str]) -> str:
    joined_titles = "\n".join(f"- {t}" for t in news_list)
    period = f"{position.startEndDate.start.year}–{position.startEndDate.end.year if position.startEndDate.end else '현재'}"

    return f"""
아래는 {position.companyName}에서 {position.title}로 재직한 포지션 설명과 해당 기간({period}) 동안의 뉴스 제목 목록입니다.

포지션 설명:
{position.description or "설명 없음"}

뉴스 제목 목록:
{joined_titles}

{TEMPLATE_NEWS_FILTER_CONDITIONS}

{TEMPLATE_NEWS_FILTER_EXAMPLE}
""".strip()
