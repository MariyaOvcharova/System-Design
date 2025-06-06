
# Travel Booking Platform

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

| Status Code | Scenario                  | Resolution Path                            |
|-------------|---------------------------|--------------------------------------------|
| **400**     | Invalid request data      | Check request body/parameters format. Example: `{ "error": "Email is required" }` |
| **401**     | Missing/expired JWT       | 1. Redirect to `/login`<br>2. Auto-refresh token via `/token/refresh` |
| **403**     | Forbidden action          | Check user permissions. Example: `{ "detail": "Permission denied" }` |
| **404**     | Resource not found        | 1. Verify UUID exists<br>2. Check URL endpoint |
| **429**     | Rate limit exceeded       | 1. Wait for next available request<br>2. Check `Retry-After` header |
| **500**     | Server error              | 1. Check Django logs<br>2. Verify database connection |

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
