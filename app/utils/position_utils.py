from datetime import datetime
from typing import Tuple
from calendar import monthrange

def parse_position_dates(position) -> Tuple[str, str]:
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
    return desc.strip().replace("\n", ", ") if desc else "설명 없음"

def build_embedding_text(position) -> str:
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
