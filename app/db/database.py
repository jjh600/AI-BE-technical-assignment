from app.config import POSTGRES_CONFIG
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    """
    PostgreSQL 연결을 생성하고 AUTOCOMMIT 모드로 설정
    """
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def get_company_id_map() -> dict[str, int]:
    """
    company 테이블에서 기업명과 ID 매핑을 가져옵니다.
    {회사명: company_id} 형태의 딕셔너리를 반환
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM company")
            rows = cursor.fetchall()
            logger.info(f"[DB] 기업 매핑 {len(rows)}건 로드됨")
            return {name: cid for cid, name in rows}
    except Exception as e:
        logger.error(f"[DB 오류] 회사 ID 맵 조회 실패: {e}")
        raise
    finally:
        conn.close()
