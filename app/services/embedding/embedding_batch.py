from app.config import EMBEDDING_MODEL
from app.db.database import get_db_connection

import logging

from app.services.embedding.embedding_service import generate_embedding, generate_embeddings_batch

logger = logging.getLogger(__name__)

def embed_table_columns(
    table: str,
    text_columns: list[str],
    id_column: str = "id",
    embedding_column: str = "embedding",
    model: str = EMBEDDING_MODEL,
    joiner: str = " ",
    batch_size: int = 1,
):
    """
    지정한 테이블의 text 컬럼들을 합쳐 OpenAI 임베딩을 생성하고,
    해당 row의 embedding 컬럼에 저장한다.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cols_str = ", ".join([id_column] + text_columns)
            null_check = f"{embedding_column} IS NULL"
            cursor.execute(f"SELECT {cols_str} FROM {table} WHERE {null_check}")
            rows = cursor.fetchall()
            fail_count = 0

            logger.info(f"{len(rows)}개의 레코드에서 임베딩을 생성합니다. (batch_size={batch_size})")

            if batch_size <= 1:
                # 단건 처리
                for row in rows:
                    row_id = row[0]
                    text_values = row[1:]
                    full_text = joiner.join([str(v) for v in text_values if v])

                    if not full_text.strip():
                        logger.warning(f"{row_id}는 텍스트가 비어 있어 건너뜁니다.")
                        continue

                    try:
                        embedding = generate_embedding(full_text, model)
                        cursor.execute(
                            f"UPDATE {table} SET {embedding_column} = %s WHERE {id_column} = %s",
                            (embedding, row_id)
                        )
                    except Exception as e:
                        logger.warning(f"{row_id} 처리 중 오류: {e}")
                        fail_count += 1
            else:
                # 배치 처리
                for i in range(0, len(rows), batch_size):
                    batch = rows[i:i + batch_size]
                    texts = []
                    valid_ids = []

                    for row in batch:
                        row_id = row[0]
                        full_text = joiner.join([str(v) for v in row[1:] if v])

                        if not full_text.strip():
                            logger.warning(f"{row_id}는 텍스트가 비어 있어 건너뜁니다.")
                            continue

                        texts.append(full_text)
                        valid_ids.append(row_id)

                    try:
                        embeddings = generate_embeddings_batch(texts, model)
                        for row_id, embedding in zip(valid_ids, embeddings):
                            cursor.execute(
                                f"UPDATE {table} SET {embedding_column} = %s WHERE {id_column} = %s",
                                (embedding, row_id)
                            )
                    except Exception as e:
                        logger.warning(f"배치 처리 중 오류 (rows {i}~{i+batch_size}): {e}")
                        fail_count += len(valid_ids)

        conn.commit()
        logger.info(f"총 {len(rows)}건 중 {fail_count}건 실패.")
        logger.info("임베딩 생성 및 저장 완료.")
    finally:
        conn.close()