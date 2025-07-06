#!/bin/bash
echo "Starting frontend server..."
echo "PORT environment variable: $PORT"
exec npx serve -s dist -p "${PORT:-3000}"