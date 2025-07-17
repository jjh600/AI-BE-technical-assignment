from datetime import datetime
from typing import Tuple
from calendar import monthrange

from app.constants import DEFAULT_POSITION_DESCRIPTION
from app.schemas.inference import Position


def parse_position_dates(position: Position) -> Tuple[str, str]:
    """
    포지션의 시작일과 종료일을 YYYY-MM-DD 형식으로 반환
    """
    start = f"{position.startEndDate.start.year}-{position.startEndDate.start.month:02}-01"
    if position.startEndDate.end:
        year = position.startEndDate.end.year
        month = position.startEndDate.end.month
        last_day = monthrange(year, month)[1]
        end = f"{year}-{month:02}-{last_day}"
    else:
        end = datetime.today().strftime("%Y-%m-%d")
    return start, end

def normalize_position_description(desc: str) -> str:
    """
    포지션 설명 문자열을 정제 (줄바꿈 제거, 공백 처리)
    """
    return desc.strip().replace("\n", ", ") if desc else DEFAULT_POSITION_DESCRIPTION

def build_embedding_text(position: Position) -> str:
    """
    포지션 정보를 기반으로 임베딩에 사용할 텍스트를 생성
    """
    start_year = position.startEndDate.start.year
    end_year = position.startEndDate.end.year if position.startEndDate.end else datetime.today().year
    period = f"{start_year}–{end_year}"

    parts = [
        f"회사명: {position.companyName.strip()}",
        f"직무: {position.title.strip()}",
    ]

    if position.description.strip():
        parts.append(f"설명: {position.description.strip().replace('\n', ' ')}")

    parts.append(f"기간: {period}")
    return ", ".join(parts)
