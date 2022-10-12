from threading import RLock


class Database(object):
    def __init__(self):
        self._database = {}
        self._lock = RLock()

    def __enter__(self, *args, **kwargs):
        self._lock.acquire()
        return self._database

    def __exit__(self, *args, **kwargs):
        self._lock.release()


database = Database()