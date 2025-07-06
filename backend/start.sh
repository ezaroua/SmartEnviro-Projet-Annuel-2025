#!/bin/bash

# Function to wait for MySQL to be ready
wait_for_mysql() {
    echo "Waiting for MySQL to be ready..."
    while ! mysqladmin ping -h"db" -P"3306" --silent; do
        echo "MySQL is not ready yet. Waiting..."
        sleep 2
    done
    echo "MySQL is ready!"
}

# Wait for database to be ready
wait_for_mysql

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting application..."
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application 