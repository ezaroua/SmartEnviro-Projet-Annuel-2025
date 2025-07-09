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

# Create models directory and copy model files
RUN mkdir -p models
COPY simplified_xgboost_weather_model.joblib ./models/
COPY simplified_weather_scaler.joblib ./models/
COPY simplified_weather_features.csv ./models/

EXPOSE 5000

# Command to run the application
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 app:app"]