import os
from flask import Flask
from flask import request, abort
from .database import database

app = Flask(__name__)


@app.get('/')
def root():
    return {
        'app': 'py-key-value-store',
        'hostname': os.uname()[1]
    }


@app.get('/doc/')
@app.get('/doc')
def index():
    with database as db:
        return list(db.keys())


@app.get('/doc/<key>')
def get_by_id(key: str):
    with database as db:
        if key in db:
            return db[key]
        else:
            return {'message': 'Not found'}, 404


@app.put('/doc/<key>')
def put(key: str):
    with database as db:
        db[key] = request.get_json()
        return {
            'status': 'Okay'
        }


@app.get('/health')
@app.get('/health/')
def health():
    return {
        'status': 'ALIVE',
        'environment': {k: v for k, v in os.environ.items()},
        'hostname': os.uname()[1]
    }


def main(*args, **kwargs):
    app.run()


if __name__ == '__main__':
    main()
