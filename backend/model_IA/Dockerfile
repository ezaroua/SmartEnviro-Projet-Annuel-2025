FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY app.py .
COPY preprocessing.py .

# Copy model files (no need to create models directory since files are already in root)
COPY simplified_xgboost_weather_model.joblib ./
COPY simplified_weather_scaler.joblib ./
COPY simplified_weather_features.csv ./

EXPOSE 5001

# Command to run the application
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 1 app:app"]