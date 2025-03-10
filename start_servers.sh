#!/bin/bash

# Start the backend API server
uvicorn main:app --host 0.0.0.0 --port 5000 &

# Wait a moment for the backend to start
sleep 2

# Start the frontend development server
cd frontend && npm run dev