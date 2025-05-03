from flask import Flask, request, jsonify
import requests
from time import time

app = Flask(__name__)

BUCKET_CAPACITY = 2
LEAK_RATE = 1.0
DJANGO_BACKEND = "http://localhost:8000/register/"  

rate_limits = {}

class LeakyBucket:
    def __init__(self):
        self.tokens = 0.0
        self.last_update = time()
    
    def allow(self):
        now = time()
        elapsed = now - self.last_update
        
        self.tokens = max(0, self.tokens - elapsed * LEAK_RATE)
        self.last_update = now
        
        if self.tokens + 1 <= BUCKET_CAPACITY:
            self.tokens += 1
            return True
        return False

def forward_to_django(method, data):
    try:
        response = requests.request(
            method=method,
            url=DJANGO_BACKEND,
            json=data,
            timeout=5
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/api', methods=['GET', 'POST'])
def api():
    client_ip = request.args.get('ip', request.remote_addr)
    
    if client_ip not in rate_limits:
        rate_limits[client_ip] = LeakyBucket()
    
    if not rate_limits[client_ip].allow():
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    data = request.get_json() if request.is_json else {}
    return forward_to_django(request.method, data)

if __name__ == '__main__':
    app.run(port=5000)