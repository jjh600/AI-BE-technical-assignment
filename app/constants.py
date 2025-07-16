MAX_TOP_K = 100
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

FILTER_THRESHOLD_SCORE = 0.3
TAG_LIST = [
    "상위권대학교", "대규모 회사 경험", "리더쉽", "해외 경험", ...
]
