# AI381 Churn Prediction MLOps

A containerized machine learning API that predicts customer churn using a trained Scikit-learn model.

[![CI](https://github.com/SKINNy2k/ai381-churn-mlops/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SKINNy2k/ai381-churn-mlops/actions/workflows/ci.yml)

## Run the project

Requirements:
- Docker
- Docker Compose

Start the API with one command:

```bash
docker compose up --build
```

The API will be available at:

- Health check: http://localhost:8000/health
- Prediction endpoint: http://localhost:8000/predict
- Interactive API documentation: http://localhost:8000/docs

To stop the service, press `Ctrl+C`.

## Machine Learning Model

The project uses a trained Scikit-learn pipeline to predict customer churn.

## CI/CD

GitHub Actions automatically:
- Runs Ruff linting.
- Runs automated tests on pull requests and pushes to `main`.
- Builds the Docker image.
- Scans the image with Trivy.
- Pushes the image to GitHub Container Registry (GHCR), tagged with the commit SHA.
