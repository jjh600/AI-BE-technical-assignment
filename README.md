# AI Experience Inference Backend (RAG-based)
후보자의 이력 데이터를 기반으로 대규모 뉴스 데이터와 LLM을 활용해 경험을 추론하는 백엔드 시스템입니다.

## 📁 프로젝트 구조
```
app/
│   ├── api/
│   │   └── v1/
│   │       └── inference.py
│   ├── config.py
│   ├── constants.py
│   ├── core/
│   │   └── rag_pipeline.py
│   ├── db/
│   │   ├── database.py
│   │   └── vector_store.py
│   ├── main.py
│   ├── schemas/
│   │   └── inference.py
│   ├── services/
│   │   ├── embedding/
│   │   │   ├── embedding_batch.py
│   │   │   └── embedding_service.py
│   │   ├── llm/
│   │   │   ├── llm_client.py
│   │   │   ├── prompt_builder.py
│   │   │   └── templates.py
│   │   └── retriever/
│   │       └── retriever_service.py
│   └── utils/
│       ├── logger.py
│       └── position_utils.py
scripts/
│   ├── embed_news_data.py
│   └── manage_vector_columns.py
tests/
│   ├── integration/
│   │   └── test_rag_flow.py
│   └── unit/
│       ├── api/
│       │   └── test_rag_api.py
│       ├── core/
│       │   └── test_rag_pipeline.py
│       ├── services/
│       │   ├── embedding/
│       │   │   └── test_embedding_service.py
│       │   ├── llm/
│       │   │   ├── test_llm_client.py
│       │   │   └── test_prompt_builder.py
│       │   └── retriever/
│       │       └── test_retriever_service.py
│       └── utils/
│           └── test_position_utils.py
docker-compose.yaml
poetry.lock
pyproject.toml
.env.example
```

## 🧠 핵심 개념

- **RAG (Retrieval-Augmented Generation)** 기반 추론
- 벡터 검색을 활용한 후보자 경험 추론
- FastAPI 기반 REST API 서버

## 🗂️ 폴더 설명

| 폴더 | 설명 |
|------|------|
| `app/api` | FastAPI 라우팅 (엔드포인트) 정의 |
| `app/core` | 추론 파이프라인 구성 로직 |
| `app/db` | DB 연결, 벡터 검색 SQL 구성 |
| `app/services` | 실제 기능 로직 (임베딩, 검색, LLM 등) |
| `app/schemas` | Pydantic 기반 입출력 모델 정의 |
| `app/utils` | 날짜 처리, 로그 등 유틸 함수 |
| `scripts/` | 데이터 임베딩, 벡터 관리 CLI |
| `tests/` | 단위 테스트 및 통합 테스트 코드 |

## 🔧 사전 설정

### 1. 환경 변수 파일 생성
`.env.example` 파일을 복사해 사용하세요.

```bash
cp .env.example .env
cp .env.example .env.dev
```
필수 항목:
- OPENAI_API_KEY
- PG_HOST, PG_PORT, PG_DATABASE, PG_USER, PG_PASSWORD
- LOG_LEVEL (개발 시에는 DEBUG 권장 - .env.dev)

### 2. Poetry 설치 및 의존성 설치
```bash
poetry install
# 운영 환경
poetry install --no-dev
```

### 3. Docker Compose로 PostgreSQL 실행
.env의 DB 설정과 docker-compose.yaml 내 포트/사용자 정보가 일치해야 합니다.
```bash
docker-compose up -d
```

### 4. 예시 데이터 삽입
회사 및 뉴스 데이터를 DB에 적재합니다.
```bash
cd example_datas
poetry run python setup_company_data.py
poetry run python setup_company_news_data.py
```

### 5. 벡터 컬럼 준비 및 임베딩 수행
```bash
cd scripts
# 벡터 컬럼 생성 (embedding 컬럼이 없다면)
poetry run python manage_vector_columns.py

# 뉴스 데이터 임베딩 (OpenAI API 호출)
poetry run python embed_news_data.py
```

## 🚀 실행 방법

```bash
# 서버 실행 (운영 환경)
PYTHONPATH=./ ENV_FILE=.env poetry run uvicorn app.main:app --reload

# 서버 실행 (개발 환경)
PYTHONPATH=./ ENV_FILE=.env.dev poetry run uvicorn app.main:app --reload

# 단위 테스트 실행
poetry run pytest tests/unit/

# 통합 테스트 실행
poetry run pytest tests/integration/
```

## 📬 주요 엔드포인트

- `POST /api/v1/inference/experience` : 이력 및 뉴스 기반 경험 추론 요청

## 📌 RAG 구성 흐름

본 프로젝트는 Retrieval-Augmented Generation (RAG) 기반으로 구성되어 있으며,  
인재의 이력 정보와 뉴스 데이터를 결합해 고급 경험을 추론합니다.

### 🔄 전체 추론 파이프라인 흐름

1. 입력된 인재 JSON을 기반으로 각 포지션별로 쿼리 문장 생성
2. pgvector 기반 벡터 검색으로 유사 뉴스 제목 Top-N 조회
3. **LLM 호출 ①**: 검색된 뉴스 제목과 LLM이 학습한 실제 뉴스 지식을 바탕으로  
   실제 존재하는 뉴스 제목만 필터링  
4. 필터링된 뉴스 제목들을 포지션 정보와 함께 다시 구성
5. **LLM 호출 ②**: 학력, 포지션 이력, 뉴스 정보를 바탕으로 경험 태그 추론
6. 태그별 간단한 근거와 함께 결과 반환

---

### 🏷️ 사전 정의된 경험 키워드

- 상위권대학교: 서울대, 연세대, 고려대 등
- 대규모 회사 경험
- 성장기 스타트업 경험
- 리더쉽
- 대용량 데이터 처리 경험
- M&A 경험
- IPO 경험
- 투자 유치 경험

## 💬 기타
### 📡 API 호출 예시
```bash
curl -X POST http://localhost/api/v1/inference/experience \
  -H "Content-Type: application/json" \
  -d @example_datas/talent_ex4.json
```
- nginx 연동이 없다면 포트를 8000 등 Uvicorn 실행 시 지정한 포트로 맞춰주세요. ex) localhost:8000
- example_datas/talent_ex4.json은 실제 예시 인재 JSON입니다.

## 🛠️ 향후 개선 방향

### 🔍 1. 벡터 검색 정확도 향상

> 현재 방식:  
> 회사명, 직무, 설명, 재직 기간을 결합한 긴 텍스트를 임베딩하여 뉴스 제목과 유사도 기반 검색

**문제점**
- 텍스트가 장황하여 벡터 유사도가 분산됨  
- 실제 관련 뉴스가 누락되는 경우 존재  

**개선 아이디어**
- **임베딩 텍스트 간소화**  
  → 회사명만 사용하거나 `회사명 + 직무명` 조합으로 축소
- **핵심 키워드 추출 기반 임베딩**  
  → 직무 설명에서 LLM 또는 규칙 기반 키워드를 추출 후 임베딩 생성
- **임베딩 모델 변경 검토**  
  → 현재 OpenAI 임베딩 모델(`text-embedding-3-small`)
- **유사도 threshold 조정**  
  → `FILTER_THRESHOLD_SCORE` 값을 0.3 → 0.2 등으로 낮춰 recall 개선

---

### 🧠 2. LLM 추론 커스터마이징

> 현재 방식:  
> 뉴스 필터링과 경험 태그 추론 모두 동일한 모델(`gpt-4o`)로 수행

**개선 아이디어**
- **역할에 따른 모델 및 파라미터 분리**  
  → 뉴스 필터링, 태그 추론 등 경량/정밀 모델 분리
- **토큰/temperature 조정**  
  → 필터링은 temperature=0, 추론은 temperature=0.3~0.5 등 적절히 조정
- **프롬프트 표현 개선**  
  → 조건, 태그 정의, 근거 작성 가이드 등을 더 명확히 정리해 LLM 일관성 확보
