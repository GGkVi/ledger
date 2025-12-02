FROM python:3.13-slim-bookworm

WORKDIR /app

# 시스템 패키지 + 한글폰트 + fontconfig 설치(슬림버전이라서)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev libyaml-dev fontconfig fonts-nanum && \
    fc-cache -fv && \
    rm -rf /var/lib/apt/lists/*

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
