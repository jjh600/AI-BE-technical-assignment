from app.db.database import get_db_connection
import logging

logger = logging.getLogger(__name__)


def add_embedding_column(table_name: str, dimension: int = 1536, column_name: str = "embedding"):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            logger.info("pgvector extension 확인 완료.")

            cursor.execute(f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = '{table_name}' AND column_name = '{column_name}'
                    ) THEN
                        ALTER TABLE {table_name} ADD COLUMN {column_name} vector({dimension});
                    END IF;
                END
                $$;
            """)
            logger.info(f"{table_name}.{column_name} 컬럼 추가 완료.")
    finally:
        conn.close()


def create_index_on_vector(table_name: str, column_name: str = "embedding", index_name: str = None, lists: int = 100):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if not index_name:
                index_name = f"{table_name}_{column_name}_idx"

            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS {index_name}
                ON {table_name}
                USING ivfflat ({column_name} vector_cosine_ops)
                WITH (lists = {lists});
            """)
            logger.info(f"{index_name} 인덱스가 생성되었습니다.")
    finally:
        conn.close()

def drop_embedding_column(table_name: str, column_name: str = "embedding"):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = '{table_name}' AND column_name = '{column_name}'
                    ) THEN
                        ALTER TABLE {table_name} DROP COLUMN {column_name};
                        RAISE NOTICE 'Dropped column {column_name} from {table_name}.';
                    ELSE
                        RAISE NOTICE 'Column {column_name} does not exist in {table_name}.';
                    END IF;
                END
                $$;
            """)
            logger.info(f"{table_name}.{column_name} 컬럼 삭제 완료 또는 존재하지 않음.")
    finally:
        conn.close()


if __name__ == "__main__":
    # drop_embedding_column("company_news")  # 임베딩 컬럼 다시 넣을 경우 컬럼 삭제 후 다시 추가
    add_embedding_column("company_news")
    # create_index_on_vector("company_news")  # index 생성
