import pytest
from unittest.mock import patch
from app.services.embedding.embedding_service import generate_embedding, generate_embeddings_batch

@patch("app.services.embedding.embedding_service.openai.embeddings.create")
def test_generate_embedding(mock_create):
    mock_create.return_value = type("MockResponse", (), {
        "data": [type("Obj", (), {"embedding": [0.1] * 1536})]
    })()

    result = generate_embedding("test text", "test-model")
    assert isinstance(result, list)
    assert len(result) == 1536

@patch("app.services.embedding.embedding_service.openai.embeddings.create")
def test_generate_embeddings_batch(mock_create):
    mock_create.return_value = type("MockResponse", (), {
        "data": [type("Obj", (), {"embedding": [0.1] * 1536}) for _ in range(2)]
    })()

    result = generate_embeddings_batch(["a", "b"], "test-model")
    assert len(result) == 2
    assert all(len(emb) == 1536 for emb in result)
