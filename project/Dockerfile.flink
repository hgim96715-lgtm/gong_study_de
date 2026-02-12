
FROM flink:1.18.1

USER root

RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    openjdk-11-jdk-headless \
    libssl-dev zlib1g-dev libffi-dev \
    ca-certificates \
    curl \
    netcat-openbsd \
    iputils-ping && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*


ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64


RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --default-timeout=1000 \
    apache-flink==1.18.1 \
    typing_extensions


RUN curl -o /opt/flink/lib/flink-sql-connector-kafka-3.0.0-1.18.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.0-1.18/flink-sql-connector-kafka-3.0.0-1.18.jar


ENV PYTHON_EXECUTABLE=/usr/bin/python3
ENV PYFLINK_CLIENT_EXECUTABLE=/usr/bin/python3

USER flink
WORKDIR /opt/flink