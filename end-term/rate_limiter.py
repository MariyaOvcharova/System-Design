from flask import Flask, request
from time import time

app = Flask(__name__)

BUCKET_CAPACITY = 2  
LEAK_RATE = 1.0     

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

@app.route('/api', methods=['GET', 'POST'])
def api():
    client_ip = request.args.get('ip', request.remote_addr)
    
    if client_ip not in rate_limits:
        rate_limits[client_ip] = LeakyBucket()
    
    if not rate_limits[client_ip].allow():
        return {"error": "Rate limit exceeded"}, 429
    
    if request.method == 'POST':
        return {"message": "User created"}, 201
    
    return {"message": "Success"}, 200

if __name__ == '__main__':
    app.run(port=5000)