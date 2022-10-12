import os
from flask import Flask
from flask import request
from threading import RLock

app = Flask(__name__)


class Database(object):
    def __init__(self):
        self._database = {}
        self._lock = RLock()

    def __enter__(self,  *args, **kwargs):
        self._lock.acquire()
        return self._database

    def __exit__(self, *args, **kwargs):
        self._lock.release()


database = Database()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.get('/doc/<key>')
def get_by_id(key: str):
    with database as db:
        return db[key]


@app.put('/doc/<key>')
def put(key: str):
    with database as db:
        db[key] = request.get_json()
        return {
            'status' : 'Okay'
        }


@app.get('/health')
def health():
    return {
        'status': 'ALIVE',
        'environment': {k: v for k, v in os.environ.items()},
        'hostname': os.uname()[1]
    }


def main():
    app.run()


if __name__ == '__main__':
    main()
