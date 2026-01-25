FROM apache/airflow:3.1.6

USER root

# 1. OpenJDK 17 설치 (Spark 통신 필수)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Java 홈 환경변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

USER airflow

# 2. Provider 패키지 설치
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt