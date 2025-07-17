# ================================
# 🔍 벡터 검색 관련 설정
# ================================

MAX_TOP_K = 100  # 유사도 검색 시 최대 반환 개수
FILTER_THRESHOLD_SCORE = 0.3  # 유사도 최소 허용 기준

DISTANCE_METRICS = {
    "cosine": {
        "symbol": "<=>",
        "similarity_expr": "1 - ({col} <=> %s::vector)",
        "where_expr": "1 - ({col} <=> %s::vector) >= %s"
    },
    "inner_product": {
        "symbol": "<#>",
        "similarity_expr": "{col} <#> %s::vector",
        "where_expr": "({col} <#> %s::vector) >= %s"
    }
}
DEFAULT_DISTANCE_METRIC = "cosine"

EMBEDDING_COLUMN = "embedding"
NEWS_TABLE = "company_news"


# ================================
# 🧠 LLM 관련 설정
# ================================

DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.3
MAX_TOKENS = 512


# ================================
# ⚙️ 일반/공통 설정
# ================================

DEFAULT_POSITION_DESCRIPTION = "설명 없음"
