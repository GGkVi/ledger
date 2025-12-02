# 💰 Ledger - 미니 프로젝트 가계부 시스템

이번 프로젝트는 Django를 이용한 가계부 만들기 프로젝트입니다. 이번 경험을 통해 팀원들끼리의 협업과 github 경험 Docker를 이용한 개발 환경 구축등의 경험을 배웠습니다.

## 📊 ERD
<img width="1566" height="1080" alt="image" src="https://github.com/user-attachments/assets/245de704-fede-4670-8723-85fd1949d463" />




## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)

## 🎯 프로젝트 소개

Ledger는 사용자의 재무 활동을 체계적으로 관리할 수 있는 가계부 시스템입니다. 
계좌 관리, 거래 내역 추적, 소비 패턴 분석 등을 통해 효율적인 재무 관리를 지원합니다.

### 프로젝트 목표

- ✓ Git/Github를 활용한 협업 경험
- ✓ Poetry를 활용한 의존성 관리 및 실행 환경 구성
- ✓ Docker 컨테이너 기반 개발 환경 구축
- ✓ PostgreSQL 데이터베이스 연동 및 ORM 활용
- ✓ ERD 설계 및 Test 코드 작성 (TDD)
- ✓ Django 웹 프레임워크 활용
- ✓ CI/CD 파이프라인 구축 (Github Actions)
- ✓ AWS EC2 배포 경험

## ✨ 주요 기능

### 1. 사용자 인증
- 회원가입 / 로그인 / 로그아웃
- 사용자 권한 관리

### 2. 계좌 관리 (CRD)
- 계좌 등록
- 계좌 조회 (전체/특정)
- 계좌 삭제

### 3. 거래 내역 (CRUD)
- 거래 내역 생성 (입금/출금)
- 거래 내역 조회
- 거래 내역 수정
- 거래 내역 삭제

### 4. 데이터 분석 및 시각화 (x)
- 주간/월간 소비 데이터 분석
- 카테고리별 지출 분석
- 데이터 시각화 (그래프/이미지)
- Celery를 통한 백그라운드 처리

### 5. 알림 기능 (x)


### 6. 관리자 기능
- Django Admin 페이지
- 전체 데이터 관리

## 🛠 기술 스택

### Backend
- **Framework**: Django 5.0+
- **Language**: Python 3.13+
- **Database**: PostgreSQL 18

### DevOps
- **Containerization**: Docker, Docker Compose
- **CI/CD**: Github Actions
- **Deployment**: AWS EC2
- **Dependency Management**: UV

### Development Tools
- **Version Control**: Git, Github
- **Code Quality**: Pre-commit hooks
- **Testing**: Django TestCase, pytest


### 주요 테이블

- **USER**: 사용자 정보 (이메일, 사용자명, 권한 등)
- **BANK_CODES**: 은행 코드 정보
- **ACCOUNTS**: 계좌 정보 (계좌번호, 용도, 은행 등)
- **TRANSACTION**: 거래 내역 (입출금, 금액, 카테고리 등)
- **BLACKLISTTOKEN**: 로그아웃된 JWT 토큰
- **ANALYSIS**: 주간/월간 소비 분석 결과
- **NOTIFICATION**: 사용자 알림

6. **서버 접속**
- 웹 서버: http://localhost:8000
- Admin 페이지: http://localhost:8000/admin
- Swagger 페이지: http://localhost:8000/

### 주요 엔드포인트

#### 사용자
- `POST /api/users/signup/` - 회원가입
- `POST /api/users/token/` - 로그인
- `POST /api/users/logout/` - 로그아웃
- `GET /api/users/profile/` - 유저 조회
- `PATCH /api/users/profile/update/` - 유저 수정 
- `DELETE /api/users/profile/delete/` - 유저 삭제

#### 계좌
- `GET /api/accounts/` - 계좌 목록 조회
- `POST /api/accounts/` - 계좌 생성
- `GET /api/accounts/{id}/` - 계좌 상세 조회
- `DELETE /api/accounts/{id}/` - 계좌 삭제

#### 거래내역
- `GET /api/transactions/` - 거래내역 목록 조회
- `POST /api/transactions/` - 거래내역 생성
- `GET /api/transactions/{id}/` - 거래내역 상세 조회
- `PATCH /api/transactions/{id}/` - 거래내역 수정
- `DELETE /api/transactions/{id}/` - 거래내역 삭제

#### 분석
- `GET /api/analysis/` - 분석 결과 조회
- `POST /api/analysis/generate/` - 분석 생성 요청

## 👥 팀 구성

**팀명**: GGㅏVㅣ

| 이름 | 역할 | 담당 업무 |
|------|------|-----------|
| **송호창** | 팀장 | 회의록 작성, Analyze 기능, 역할 분배, 발표 자료 준비, 발표 |
| **강지민** | 팀원 | Docker 세팅, CI 세팅, Account 기능, Notifications 기능, format.sh 작성 |
| **박성우** | 팀원 | Pre-commit, Transactions 기능, 배포 |
| **김민규** | 팀원 | Docker 세팅, User 기능, 배포 |


## 📝 개발 단계

### 1단계: 환경 설정
- ✅ Docker 개발 환경 구축
- ✅ Git 협업 환경 설정
- ✅ 프로젝트 구조 및 규칙 정립

### 2단계: ERD 설계 및 모델 생성
- ✅ ERD 설계
- ✅ Django 모델 생성

### 3단계: API 개발
- ✅ API 스펙 작성
- ✅ 회원/인증 API
- ✅ 계좌 관리 API
- ✅ 거래내역 API


### 4단계: 데이터 분석 및 백그라운드 작업
- ✅ 주간/월간 소비 분석
- ✅ 데이터 시각화
- ✅ 스케줄링 구현

### 5단계: 알림 기능
- ✅ 알림 시스템 구현
- ✅ 읽음/안읽음 처리

### 6단계: 배포
- ✅ CI/CD 파이프라인 구축
- ✅ AWS EC2 배포

