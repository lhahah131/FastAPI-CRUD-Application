ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION}

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 100 --retries 10 -r requirements.txt

COPY ./app ./app
COPY test.py .
RUN useradd --create-home --shell /usr/sbin/nologin appuser && \
    chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

