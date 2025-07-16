from typing import List, Optional, Dict, Any

from app.constants import MAX_TOP_K, DISTANCE_METRICS, DEFAULT_DISTANCE_METRIC, FILTER_THRESHOLD_SCORE
from app.db.database import get_db_connection

import logging

logger = logging.getLogger(__name__)

def build_similarity_query_parts(embedding_column: str, metric: str = DEFAULT_DISTANCE_METRIC):
    if metric not in DISTANCE_METRICS:
        logger.warning(f"[Metric 오류] 지원하지 않는 메트릭: {metric}")
        raise ValueError(f"Unsupported metric: {metric}")

    config = DISTANCE_METRICS[metric]
    similarity_expr = config["similarity_expr"].format(col=embedding_column)
    where_expr = config["where_expr"].format(col=embedding_column)
    return similarity_expr, where_expr

def retrieve_similar_rows(
    table: str,
    embedding_column: str,
    query_embedding: List[float],
    id_column: str = "id",
    filters: Optional[Dict[str, Any]] = None,
    top_k: int = MAX_TOP_K,
    distance_metric: str = DEFAULT_DISTANCE_METRIC,
    similarity_threshold: float = FILTER_THRESHOLD_SCORE,
):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            similarity_expr, where_similarity_expr = build_similarity_query_parts(embedding_column, distance_metric)
            values = [query_embedding, query_embedding, similarity_threshold]
            logger.debug(f"[쿼리 생성] similarity_expr: {similarity_expr}")
            logger.debug(f"[쿼리 생성] where_clause: {where_similarity_expr}")

            # 기본 WHERE 절
            where_clauses = [f"{embedding_column} IS NOT NULL", where_similarity_expr]

            # 추가 필터 처리
            if filters:
                for key, val in filters.items():
                    if " " in key:  # 예: "news_date >="
                        where_clauses.append(f"{key} %s")
                    else:
                        where_clauses.append(f"{key} = %s")
                    values.append(val)

            where_sql = " AND ".join(where_clauses)

            query = f"""
                SELECT {id_column}, title, {similarity_expr} AS similarity
                FROM {table}
                WHERE {where_sql}
                ORDER BY similarity DESC
                LIMIT %s
            """
            values.append(top_k)

            cursor.execute(query, values)
            rows = cursor.fetchall()

            logger.info(f"유사도 검색 결과 {len(rows)}건 반환됨.")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"상위 5건")
                for i, (id, title, score) in enumerate(rows[:5]):
                    logger.debug(f"{i + 1}. [score={score:.3f}] {title}")
            return rows
    except Exception as e:
        logger.error(f"[DB 오류] 유사도 검색 중 오류 발생: {e}")
        raise
    finally:
        conn.close()