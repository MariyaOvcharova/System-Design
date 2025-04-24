# API Rate Limiter with Leaky Bucket

Microservice for limiting the number of API requests using the **Leaky Bucket** algorithm.  
Protects against overloads and DDoS attacks, ensuring stable operation.

Leaky Bucket algorithm for smooth load distribution
Configurable limit settings
Support for GET/POST requests

### Требования:
- Python 3.8+
- Flask

1. Установите зависимости:
   ```bash
   pip install flask

# To run the server
  python rate_limiter.py

## For test use Postman 

**GET: http://localhost:5000/api?ip=123.45.67.89**

  {
      "message": "Success"
  }

By cheking more than 2 times per second you will resive 

  {
      "error": "Rate limit exceeded"
  }

