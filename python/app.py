from abc import ABC

from api import app

if __name__ == '__main__':
    bind = '0.0.0.0:8000'
    workers = 4
    worker_class = 'gevent'
    timeout = 120
    loglevel = 'info'
    accesslog = '-'
    errorlog = '-'

    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication, ABC):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': bind,
        'workers': workers,
        'worker_class': worker_class,
        'timeout': timeout,
        'loglevel': loglevel,
        'accesslog': accesslog,
        'errorlog': errorlog,
    }
    StandaloneApplication(app, options).run()
