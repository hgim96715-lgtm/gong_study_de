
## 프로젝트 개요

**[Airflow + Kafka + Flink + Spark + Cassandra + MinIO]** 기반의 대용량 데이터 처리 파이프라인 구축 프로젝트입니다. 
배치(Batch) 처리와 스트리밍(Streaming) 처리를 모두 아우르는 실습을 목표로 하며, 모든 환경은 Docker Compose를 통해 로컬에서 실행됩니다.

---

## 구성 요소

|**컴포넌트**|**역할**|**포트 (External)**|**비고**|
|---|---|---|---|
|**Airflow**|워크플로우 관리 및 스케줄링|`8080`|Executor: Celery|
|**Kafka**|실시간 메시지 브로커|`29092`|Internal: 9092|
|**Flink**|실시간 스트리밍 처리|`8081`|Job Manager|
|**Spark**|대용량 배치 처리|`9090`|Master UI (포트 변경됨)|
|**Cassandra**|분산 NoSQL 저장소|`9042`|CQL|
|**MinIO**|S3 호환 오브젝트 스토리지|`9001`|Console|


---
## 대시보드 접속 (Dashboards)

> [!INFO] **로그인 정보 확인** `docker-compose.yaml` 설정에 따른 기본 계정 정보입니다.

### 1. Airflow (워크플로우)

- **URL:** [http://localhost:8080](https://www.google.com/search?q=http://localhost:8080)
- **ID / PW:** `airflow` / `airflow`

### 2. Flink (스트리밍)

- **URL:** [http://localhost:8081](https://www.google.com/search?q=http://localhost:8081)
- **상태:** Task Slots 확인 필요

### 3. Spark Master (배치)

- **URL:** [http://localhost:9090](https://www.google.com/search?q=http://localhost:9090)
- **주의:** 기본 포트(8080) 충돌 방지를 위해 **9090**으로 변경됨.

### 4. MinIO (S3 스토리지)

- **URL:** [http://localhost:9001](https://www.google.com/search?q=http://localhost:9001)
- **ID / PW:** `minioadmin` / `minioadmin`


---
## 환경 설정 전략 (Requirements 분리)

각 컴포넌트는 **실행 환경과 역할이 서로 다르기 때문에** Python 의존성을 분리하여 관리합니다. 
이를 통해 버전 충돌을 방지하고 컨테이너별 최적화를 유지합니다.

- **`requirements.txt`**
    - **용도:** Airflow (워크플로우 오케스트레이션)
    - **내용:** Airflow Providers, 공통 유틸리티

- **`requirements_spark.txt`**
    - **용도:** Spark (배치 처리 / PySpark Job)
    - **내용:** PySpark 3.5.x, Pandas, PyArrow,numpy

- **`requirements_flink.txt`**
    - **용도:** Flink (스트리밍 처리 / PyFlink Job)
    - **내용:** Apache-Flink 1.18.x, Kafka-Python 2.0.x, pandas,numpy


---
## Quick Start Commands

```bash
# 전체 시스템 실행
docker-compose up -d

# Docker에 변경이 있다면 
docker-compose up -d --build

#  전체 시스템 종료 
docker-compose down

#  전체 초기화 (데이터 삭제 주의 )
docker-compose down --volumes --rmi all
```
