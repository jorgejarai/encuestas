from flask import Flask
from flask_pymongo import PyMongo


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    """Almacena una instancia de PyMongo para uso en otras clases"""
    pymongo: PyMongo

    def setup(self, app: Flask):
        """Configura la instancia actual de PyMongo"""
        self.pymongo = PyMongo(app)
