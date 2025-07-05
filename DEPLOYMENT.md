# SmartEnviro Deployment Guide

## Quick Start with Railway

### 1. Deploy Backend
```bash
cd backend
railway login
railway init
railway up
```

### 2. Add PostgreSQL Database
- Go to Railway dashboard
- Click "Add Service" → "Database" → "PostgreSQL"
- Railway will automatically set `DATABASE_URL` environment variable

### 3. Set Environment Variables
In Railway dashboard, set:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=.railway.app
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.railway.app
```

### 4. Run Database Migrations
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### 5. Deploy Frontend
```bash
cd frontend
railway init
railway up
```

Set frontend environment variable:
```
VITE_API_URL=https://your-backend-domain.railway.app
```

## Docker Development

### Start Development Environment
```bash
# Clone repository
git clone <repository-url>
cd SmartEnviro-Projet-Annuel-2025

# Start all services
docker-compose -f docker-compose.dev.yml up --build

# Access:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# Database: localhost:5432
```

### Production Build
```bash
# Build and run production containers
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Manual Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend (.env)
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app
DATABASE_URL=postgresql://user:password@localhost:5432/smartenviro
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend (.env)
```
VITE_API_URL=https://your-backend-url.railway.app
```

## Troubleshooting

### Common Issues
1. **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in backend settings
2. **Database connection**: Verify `DATABASE_URL` format
3. **Static files**: Run `python manage.py collectstatic` for production
4. **Railway build fails**: Check `nixpacks.toml` configuration

### Health Check
- Backend: `GET /health/` should return `{"status": "healthy"}`
- Frontend: Should load without console errors

### Database Reset
```bash
# Development
rm db.sqlite3
python manage.py migrate

# Production (Railway)
railway run python manage.py flush
railway run python manage.py migrate
```