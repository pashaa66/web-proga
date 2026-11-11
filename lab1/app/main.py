import os

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()
users = []


class User(BaseModel):
    name: str
    email: str


@app.get('/')
def root():
    return {'message': 'Hello from Docker!', 'db_host': os.getenv('DB_HOST')}


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/api/users')
def list_users():
    return {'users': users}


@app.post('/api/users', status_code=201)
def create_user(user: User):
    users.append(user)
    return user


@app.api_route('/debug', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
async def debug(request: Request):
    body = await request.body()
    return {
        'method': request.method,
        'path': request.url.path,
        'headers': dict(request.headers),
        'body': body.decode(),
    }
