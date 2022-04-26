from bson.objectid import ObjectId
from db import Singleton, Database


class Surveys(metaclass=Singleton):
    def get_all(self):
        """Obtiene una lista con todas las encuestas"""
        ret = list(Database().pymongo.db.surveys.find())

        if ret:
            for survey in ret:
                survey['_id'] = str(survey['_id'])

        return ret

    def get_by_id(self, id):
        """Busca una encuesta a partir de su ID. Retorna None si no la encuentra"""
        ret = Database().pymongo.db.surveys.find_one({"_id": ObjectId(id)})

        if ret:
            ret['_id'] = str(ret['_id'])

        return ret

    def create(self, **kwargs):
        """Crea una encuesta a partir de **kwargs.

        Ejemplo: Surveys().create(title="Encuesta de satisfacción",
            interests=["my-bank-clients", "account-holders"],
            questions=[
                {
                    "position": 1,
                    "label": "Le gusta nuestro banco?",
                    "type": "selection",
                    "options": [
                        {
                            "value": True
                            "label": "Sí"
                        },
                        {
                            "value": False
                            "label": "No"
                        },
                    ]
                }
            ]
        """

        Database().pymongo.db.users.insert_one(kwargs)

        return kwargs

    def update(self, id, survey):
        """Actualiza los datos de una encuesta con determinado ID

        Ejemplo: si tenemos una encuesta con ID 3456 y título "Enucesta de
            satisfaczion", podemos corregir esto último con

            Surveys().update("3456", {"title": "Encuesta de satisfacción"})

            Todos los demás atributos se conservan.
        """
        Database().pymongo.db.surveys.update_one({"_id": id}, {"$set": survey})

    def delete(self, id):
        """Elimina los datos de una encuesta con determinado ID"""
        Database().pymongo.db.surveys.delete_one({"_id": id})
