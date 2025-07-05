# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SmartEnviro is a smart city environmental monitoring and prediction platform that collects, analyzes, and visualizes real-time data on pollution, weather, and traffic to optimize citizens' quality of life.

## Architecture

This is a full-stack application with:
- **Backend**: Django REST API with JWT authentication
- **Frontend**: Vue.js 3 SPA with Vite
- **Database**: MySQL (production) / SQLite (development)
- **Deployment**: Docker containers with docker-compose

### Key Components

- **User Management**: Role-based system (admin/citizen) with custom User model
- **Authentication**: JWT tokens with refresh mechanism
- **Data Apps**: Structured Django apps for users, prediction, data ingestion, and alerts
- **Frontend Structure**: Vue 3 with Pinia state management, Vue Router, and role-based layouts

## Development Commands

### Frontend (Vue.js)
```bash
cd frontend
npm install          # Install dependencies
npm run dev          # Start development server (http://localhost:5173)
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend (Django)
```bash
cd backend
pip install -r requirements.txt    # Install dependencies
python manage.py migrate           # Apply database migrations
python manage.py runserver         # Start development server (http://localhost:8000)
python manage.py createsuperuser   # Create admin user
python manage.py collectstatic     # Collect static files
```

### Docker Development
```bash
docker-compose -f docker-compose.dev.yml up --build    # Start full stack
docker-compose -f docker-compose.dev.yml down          # Stop containers
```

### Database Management
```bash
python manage.py makemigrations    # Create migrations
python manage.py migrate           # Apply migrations
python manage.py shell             # Django shell
```

## Project Structure

### Backend Apps
- `users/`: Custom user model with role-based permissions
- `prediction/`: ML prediction models and algorithms
- `data/`: Data ingestion and processing
- `alerts/`: Notification system for environmental alerts

### Frontend Organization
- `layouts/`: Role-based layouts (Public, Dashboard, Admin)
- `views/`: Page components organized by user role
- `store/`: Pinia stores for state management
- `api/`: HTTP client configuration and endpoints

## Authentication Flow

1. Users authenticate via JWT tokens
2. Role-based routing: admin (role=1) vs citizen (role=2)
3. Token stored in localStorage with automatic refresh
4. Protected routes check both token and role permissions

## Environment Configuration

### Backend (.env)
- `DEBUG`: Development mode toggle
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated allowed hosts
- `CORS_ALLOWED_ORIGINS`: Frontend URLs for CORS

### Frontend (environment variables)
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)

## Database Schema

- Custom User model extends AbstractBaseUser
- Role-based permissions with ForeignKey relationship
- MySQL compatibility with existing database schema
- Uses `db_table` meta options for table naming

## API Endpoints

Authentication endpoints are JWT-based with the following structure:
- Authentication: `/api/auth/` endpoints
- User management: `/api/users/` endpoints
- Role-based access control throughout the API

## Development Notes

- Backend uses custom user model with role-based permissions
- Frontend has role-based layouts and routing
- CORS configured for development (localhost:5173)
- Static files handled by WhiteNoise in production
- Database migrations manage schema changes
- Docker setup available for full-stack development