# insuranceprediction_adapted-with-fast-api-and-dockerise-it
Insurance Price Prediction API (FastAPI + Docker)
This project is a machine learning-powered insurance price prediction system, served via FastAPI and fully Dockerized for easy deployment and scalability.

It allows users to input features like age, gender, BMI, smoking status, and region to predict the insurance premium using a trained regression model.

🔧 Tech Stack
FastAPI – High-performance web framework for serving ML models as REST APIs

scikit-learn – For training and serializing the regression model

Docker – For containerizing the application

Uvicorn – ASGI server to run FastAPI

Jinja2 (optional) – For rendering HTML templates (optional web UI)

Features
ML Model: Trained using a dataset of insurance charges with preprocessing pipeline

API Endpoint: Predict charges using JSON input

Web UI (Optional): Simple form interface to interact with the API

Dockerized: Run with a single command (docker-compose up or docker run)

Cross-platform: Works on Windows, macOS, and Linux with Docker installed
