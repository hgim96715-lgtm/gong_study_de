# 1. 안정적인 버전 (Flink 1.18.1)
FROM flink:1.18.1-scala_2.12

USER root

# 2. 필수 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    ca-certificates \
    curl && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# 3. PyFlink 설치 (Flink 1.18.1에 맞는 버전)
RUN pip3 install --no-cache-dir \
    apache-flink==1.18.1 \
    typing_extensions

# 4. 환경 변수 설정
ENV PYTHON_EXECUTABLE=/usr/bin/python3
ENV PYFLINK_CLIENT_EXECUTABLE=/usr/bin/python3

USER flink
WORKDIR /opt/flink