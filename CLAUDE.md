# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
SmartEnviro is an intelligent environmental monitoring and prediction platform for smart cities. It collects, analyzes, and visualizes real-time data on pollution, weather, and traffic to optimize citizen quality of life.

## Architecture
- **Frontend**: Vue.js 3 SPA with Vite build tool
- **Backend**: Django REST API with JWT authentication
- **Database**: SQLite (development)
- **Authentication**: JWT tokens with role-based access (admin/citizen)

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
python manage.py runserver          # Start Django server (http://localhost:8000)
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py collectstatic      # Collect static files
```

## Key Architecture Patterns

### Backend Structure
- **Modular Django Apps**: `users`, `data`, `prediction`, `alerts`
- **Custom User Model**: Role-based authentication with `User` and `Role` models
- **JWT Authentication**: Using `rest_framework_simplejwt`
- **CORS Configuration**: Configured for frontend at localhost:5173

### Frontend Structure
- **Layout-based Routing**: Separate layouts for public, citizen dashboard, and admin
- **Role-based Navigation**: Routes protected by authentication and role checks
- **Component Architecture**: Reusable components in `/components`
- **State Management**: Vuex store (currently minimal setup)

### Key Frontend Components
- **Layouts**: `PublicLayout`, `DashboardLayout`, `AdminLayout`
- **Views**: Role-specific views in `/views/admin/` and `/views/citizen/`
- **Router Guards**: Authentication and role-based route protection

### Authentication Flow
- JWT tokens stored in localStorage
- Role stored as numeric ID (1=admin, 2=citizen)
- Route protection based on `meta.requiresAuth` and `meta.role`

## Database Schema
- **Users**: Custom user model with role-based permissions
- **Roles**: Admin and citizen roles with descriptions
- **Other apps**: `data`, `prediction`, `alerts` models are currently empty

## Development Notes
- Frontend runs on port 5173 (Vite default)
- Backend runs on port 8000 (Django default)
- CORS is configured to allow frontend-backend communication
- Currently using SQLite for development (see `backend/config/settings.py`)
- The project uses French language settings (`LANGUAGE_CODE = 'fr-fr'`)

## Testing
No specific test commands are configured in package.json. Use Django's built-in test runner:
```bash
python manage.py test
```

## Docker Setup

### Development Environment
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.dev.yml up --build

# Run individual services
docker-compose -f docker-compose.dev.yml up backend
docker-compose -f docker-compose.dev.yml up frontend
```

### Production Environment
```bash
# Build and run production setup
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Individual Docker Commands
```bash
# Backend
cd backend
docker build -t smartenviro-backend .
docker run -p 8000:8000 smartenviro-backend

# Frontend Development
cd frontend
docker build -f Dockerfile.dev -t smartenviro-frontend-dev .
docker run -p 5173:5173 smartenviro-frontend-dev

# Frontend Production
cd frontend
docker build -f Dockerfile.prod -t smartenviro-frontend-prod .
docker run -p 80:80 smartenviro-frontend-prod
```

