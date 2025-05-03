
# Travel Booking Platform

## System Overview
Platform for booking tours with:
- High load support (Black Friday, holidays)
- Multimedia content (tour photos via AWS S3)
- JWT authentication and booking system

## Functional Requirements

| Requirement                  | Implementation Details |
|------------------------------|-----------------------|
| **User Registration**        | Django `RegisterSerializer` + JWT. Rate-limited by Flask LB (2 req/sec per IP). |
| **Tour Management**          | CRUD via `TourSerializer`, photos stored in AWS S3. |
| **Booking System**           | Unique bookings enforced by `UniqueConstraint` in `Booking` model. |
| **Reviews & Ratings**        | Auto-updated tour ratings via `update_rating()`. |
| **Admin Portal**             | Django Admin + `drf-spectacular` docs. |

## Non-Functional Requirements

| Requirement                  | Implementation |
|------------------------------|----------------|
| **Availability 99.9%**       | Docker + Nginx |
| **Security**                 | HTTPS, JWT, Django ORM SQL injection protection |
| **Scalability**              | Flask load balancer + horizontal scaling |
| **API Response <1s**         | Optimized queries (`prefetch_related`) |

## Business Metrics

| Metric                      | Target       | Implementation |
|-----------------------------|--------------|----------------|
| Registered Users            | 10M+         | PostgreSQL sharding |
| Peak Bookings/Day           | >1M          | Redis caching |
| Fraud Prevention Rate       | -80%         | Unique booking constraints |

## Technology Stack

### Frontend (Angular)
- **Why Angular?**
  - Full-featured framework for complex SPAs
  - PWA support for offline mode
  - Built-in `HttpInterceptor` for JWT

### Backend (Django)
- **Key Advantages:**
  - Rapid API development with DRF
  - Built-in auth (`django.contrib.auth`)
  - Optimized queries via `TourManager`

### Load Balancer (Flask)
- **Critical for:**
  - Black Friday traffic spikes
  - Leaky Bucket algorithm (2 req/sec)
  - Health checks and request proxying

## Database Architecture

PostgreSQL Schema:
auth_user → bookings
         → reviews
tours → photo_urls (JSON) → AWS S3`

## Docker Setup

dockerfile
version: '3.8'

services:
  ### NGINX as reverse proxy
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./ssl:/etc/ssl
    depends_on:
      - flask-lb
      - django 

  ### Flask Load Balancer
  flask-lb:
    build: ./load_balancer
    ports:
      - "5000:5000"
    environment:
      - BUCKET_CAPACITY=2
      - LEAK_RATE=1.0
    depends_on:
      - django

  ### Django Backend
  django:
    build: ./backend
    command: gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - ./backend:/app
    environment:
      - DB_HOST=postgres
      - DB_NAME=travel
      - DB_USER=admin
      - DB_PASS=securepassword
    depends_on:
      - postgres
      - redis

  ### PostgreSQL Database
  postgres:
    image: postgres:14
    volumes:
      - pg_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: travel
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: securepassword

  ### Redis for caching
  redis:
    image: redis:6
    ports:
      - "6379:6379"

  ### Celery for async tasks
  celery:
    build: ./backend
    command: celery -A core worker --loglevel=info
    depends_on:
      - django
      - redis

volumes:
  pg_data:


### Database Architecture

PostgreSQL Schema:
auth_user → bookings
         → reviews
tours → photo_urls (JSON) → AWS S3

Key Tables:
1. auth_user - Django's default user model
   - id, username, email, password

2. tours - Tour information
   - id (UUID), name, description, price
   - start_date, end_date, rating
   - photo_urls (JSON array of S3 URLs)

3. bookings - User reservations
   - id (UUID), user_id (FK), tour_id (FK)
   - booking_date, status
   - UniqueConstraint (user_id + tour_id)

4. reviews - User feedback
   - id (UUID), user_id (FK), tour_id (FK)
   - rating (1-5), comment, created_at


## Error Handling

HTTP Status Codes Overview:
┌─────────┬───────────────────────────┬─────────────────────────────────────────────┐
│ Status  │ Scenario                  │ Resolution Path                            │
├─────────┼───────────────────────────┼─────────────────────────────────────────────┤
│ 400     │ Invalid request data      │ Check request body/parameters format       │
│         │ (validation errors)       │ Example: { "error": "Email is required" }  │
├─────────┼───────────────────────────┼─────────────────────────────────────────────┤
│ 401     │ Missing/expired JWT       │ 1. Redirect to /login                      │
│         │                           │ 2. Auto-refresh token via /token/refresh   │
├─────────┼───────────────────────────┼─────────────────────────────────────────────┤
│ 403     │ Forbidden action          │ Check user permissions                     │
│         │ (e.g., admin-only area)   │ Example: { "detail": "Permission denied" } │
├─────────┼───────────────────────────┼─────────────────────────────────────────────┤
│ 404     │ Resource not found        │ 1. Verify UUID exists                      │
│         │                           │ 2. Check URL endpoint                      │
├─────────┼───────────────────────────┼─────────────────────────────────────────────┤
│ 429     │ Rate limit exceeded       │ 1. Wait for next available request         │
│         │ (Flask LB protection)     │ 2. Check Retry-After header                │
├─────────┼───────────────────────────┼─────────────────────────────────────────────┤
│ 500     │ Server error              │ 1. Check Django logs                       │
│         │                           │ 2. Verify database connection              │
└─────────┴───────────────────────────┴─────────────────────────────────────────────┘

Common Error Responses:
1. JWT Expired:
   ```json
   {
     "code": "token_not_valid",
     "detail": "Token is invalid or expired",
     "messages": [
       {
         "token_class": "AccessToken",
         "message": "Token is invalid or expired"
       }
     ]
   }

### Getting Started

# 1. Clone repository
git clone https://github.com/your-repo/travel-platform.git
cd travel-platform

# 2. Build and start containers
docker-compose up -d --build

# 3. Apply database migrations
docker-compose exec django python manage.py migrate

# 4. Create admin user
docker-compose exec django python manage.py createsuperuser

# 5. Start Angular dev server (separate terminal)
cd frontend && ng serve
