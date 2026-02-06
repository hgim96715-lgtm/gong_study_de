FROM flink:2.2.0-scala_2.12

USER root

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    ca-certificates \
    curl && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# PyFlink 런타임에 필요한 최소 의존성만
RUN pip3 install --no-cache-dir --break-system-packages \
    typing_extensions

ENV PYTHON_EXECUTABLE=/usr/bin/python3
ENV PYFLINK_CLIENT_EXECUTABLE=/usr/bin/python3

USER flink
WORKDIR /opt/flink
