from app.schemas.rag import InferenceInput, InferenceOutput
from app.services.retriever.retriever_service import retrieve_news_for_position
from app.services.llm.prompt_builder import build_news_filter_prompt, generate_fixed_tags_prompt
from app.services.llm.llm_client import filter_relevant_news_from_prompt, infer_experiences_from_prompt
from app.db.database import get_company_id_map
import logging

logger = logging.getLogger(__name__)

def filter_news_for_position(position, company_map) -> list[str]:
    logger.info(f"[뉴스 필터링 시작] {position.companyName} - {position.title}")

    candidate_news = retrieve_news_for_position(position, company_map)
    logger.debug(f"[{position.title}] 검색된 뉴스 개수: {len(candidate_news)}")

    prompt = build_news_filter_prompt(position, candidate_news)
    filtered_news = filter_relevant_news_from_prompt(prompt)
    logger.info(f"[{position.title}] 필터링된 뉴스 개수: {len(filtered_news)}")

    return filtered_news

def prepare_all_filtered_news(input_data: InferenceInput) -> list[list[str]]:
    company_map = get_company_id_map()
    all_news = []

    for position in input_data.positions:
        filtered = filter_news_for_position(position, company_map)
        all_news.append(filtered)

    return all_news

def generate_tag_inference_prompt(input_data: InferenceInput, all_news: list[list[str]]) -> str:
    prompt = generate_fixed_tags_prompt(input_data, all_news)
    return prompt

def run_experience_inference(prompt: str) -> list[str]:
    experiences = infer_experiences_from_prompt(prompt)
    logger.info(f"[경험 태그 추론 완료] 추출된 태그 수: {len(experiences)}")
    return experiences

def process_inference_pipeline(input_data: InferenceInput) -> InferenceOutput:
    all_news_per_position = prepare_all_filtered_news(input_data)
    prompt = generate_tag_inference_prompt(input_data, all_news_per_position)
    experiences = run_experience_inference(prompt)
    return InferenceOutput(experiences=experiences)
