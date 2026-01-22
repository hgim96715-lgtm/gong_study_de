FROM python:3.12-slim

WORKDIR /workspace

# Jupyter + 필수 라이브러리 + pandas 관련 패키지
RUN pip install --no-cache-dir \
    jupyterlab \
    notebook \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    plotly

# requirements.txt가 있는 경우에만 설치 (선택적)
COPY requirements.txt* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

EXPOSE 8888

CMD ["jupyter", "lab","--ip=0.0.0.0","--port=8888","--no-browser","--allow-root","--ServerApp.token=","--ServerApp.password=","--ServerApp.allow_origin=*"]
