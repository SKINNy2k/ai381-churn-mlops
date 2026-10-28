
# Stage 1: Build and install Python dependencies
FROM python:3.12.10-slim-bookworm AS builder

WORKDIR /install

COPY requirements-docker.txt .

RUN pip install --no-cache-dir --prefix=/install/packages \
    -r requirements-docker.txt


# Stage 2: Final runtime image
FROM python:3.12.10-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /install/packages /usr/local

# Copy the API package and trained model
COPY src/ ./src/
COPY model.joblib .

# Create an unprivileged user
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Check whether the API is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
