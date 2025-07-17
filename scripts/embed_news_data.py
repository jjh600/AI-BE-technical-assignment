from app.services.embedding.embedding_batch import embed_table_columns

if __name__ == "__main__":
    embed_table_columns(
        table="company_news",
        text_columns=["title"],
        batch_size=100  # 배치 사이즈 지정
    )
