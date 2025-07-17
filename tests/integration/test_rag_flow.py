import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
from app.schemas.inference import ExperienceInferenceOutput

client = TestClient(app)

@patch("app.api.v1.inference.run_experience_pipeline")
def test_experience_flow(mock_pipeline):
    # 가짜 추론 결과
    mock_pipeline.return_value = ExperienceInferenceOutput(experiences=["리더쉽", "대규모 회사 경험"])

    sample_input = {
        "headline": "백엔드 개발자",
        "summary": "클라우드 기반 데이터 파이프라인 구축 경험",
        "skills": ["Python", "GCP", "Docker"],
        "positions": [
            {
                "title": "백엔드 개발자",
                "companyName": "ABC 스타트업",
                "description": "서버 개발 및 배포 자동화",
                "startEndDate": {
                    "start": {"year": 2022, "month": 1},
                    "end": {"year": 2023, "month": 6}
                }
            }
        ]
    }

    response = client.post("/api/v1/inference/experience", json=sample_input)

    assert response.status_code == 200
    data = response.json()
    assert "experiences" in data
    assert data["experiences"] == ["리더쉽", "대규모 회사 경험"]
