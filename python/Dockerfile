FROM python:3.12-slim

WORKDIR /workspace

# 필수 패키지
RUN pip install --no-cache-dir \
    jupyterlab \
    notebook

# Jupyter 실행 포트
EXPOSE 8888

# Jupyter Lab 실행,
# 토큰 없이 접속 허용-> --NotebookApp.token=""
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root","--NotebookApp.token="]
