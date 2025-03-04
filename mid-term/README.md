So, my project is enplementing saga algorithm (I've used saga orchestration algorithm) 

Also I've used:
FastAPI: A modern, high-performance web framework for building APIs with Python
Uvicorn: A lightweight ASGI server used to run the FastAPI application
Python Logging: Built-in logging module for tracking application events
Enums: Used to define and manage order statuses (e.g., "pending", "success", "failed")

To start API you should folow this steps:
1. pip install fastapi uvicorn
2. uvicorn saga:app --reload

and open http://127.0.0.1:8000/docs to manege 

