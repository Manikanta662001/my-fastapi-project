# FastAPI Auth Project

## Features

- JWT Authentication
- Refresh Tokens
- Role-Based Access
- CRUD APIs
- MongoDB Integration

## Run Project

pip install -r requirements.txt
uvicorn app.main:app --reload --> to run on http

## to Run Server(Project) on https

open git bash with path as current project and run below command
--> openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
to run the server
--> uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem --reload
