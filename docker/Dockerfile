FROM python:3.13-slim

WORKDIR /app

# Poetry 설치 캐시 사용 안함
RUN pip install --no-cache-dir poetry

# poetry 가상환경 Default 실행 안함
RUN poetry config virtualenvs.create false

# 의존성 파일 복사 컨테이너에 복사
COPY pyproject.toml poetry.lock* ./

# 의존성 설치
RUN poetry install --no-root --no-interaction -vvv

# 전체 코드 복사
COPY . .

# 실행
CMD ["poetry", "run", "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8080"]
