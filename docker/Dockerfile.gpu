# https://github.com/Kaggle/docker-python/releases
FROM gcr.io/kaggle-gpu-images/python:latest

WORKDIR /workspace
ENV KAGGLE_CONFIG_DIR=/workspace/.kaggle

# その他のライブラリ
RUN pip install --no-cache-dir \
    ruff \
    hydra-core \
    python-dotenv
