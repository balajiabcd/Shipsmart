FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --break-system-packages \
    scikit-learn \
    xgboost \
    lightgbm \
    pandas \
    numpy \
    joblib \
    fastapi \
    uvicorn

COPY models/ ./models/
COPY src/ml_models/ ./src/ml_models/

ENV PYTHONPATH=/app
ENV MODEL_PATH=/app/models

EXPOSE 8001

CMD ["uvicorn", "src.ml_models.serve:app", "--host", "0.0.0.0", "--port", "8001"]