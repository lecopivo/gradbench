FROM python:3.11-slim

RUN pip install numpy==1.26.0 pydantic dataclasses-json && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

WORKDIR /home/gradbench

COPY python /home/gradbench/python
ENV PYTHONPATH=/home/gradbench/python/gradbench

ENTRYPOINT ["python", "/home/gradbench/python/gradbench/gradbench/evals/kmeans/run.py"]
LABEL org.opencontainers.image.source=https://github.com/gradbench/gradbench
