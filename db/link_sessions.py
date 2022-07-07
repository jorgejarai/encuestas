from db import Singleton, Database
from datetime import datetime
from uuid import uuid4
from bson import ObjectId


class LinkSessions(metaclass=Singleton):
    def add(self, email: str, survey: str):
        """Genera una sesión de link a la base de datos. Retorna un link
        de login automático para el usuario especificado."""

        secret = str(uuid4())

        user_id = Database().pymongo.db.users.find_one({"email": email})["_id"]

        Database().pymongo.db.link_sessions.insert_one({
            "user": user_id,
            "time": datetime.utcnow().timestamp(),
            "duration": 60 * 60 * 24 * 7,
            "secret": secret,
            "survey_id": ObjectId(survey)
        })

        return f"login_link?secret={secret}"

    def check(self, secret: str):
        """Comprueba si un link de sesión es válido. Retorna True si es
        válido, False en caso contrario."""

        ret = Database().pymongo.db.link_sessions.find_one({"secret": secret})

        if not ret:
            return None

        if ret["time"] + ret["duration"] < datetime.utcnow().timestamp():
            return None

        return ret

    def delete(self, secret: str):
        """Elimina un link de sesión de la base de datos."""

        Database().pymongo.db.link_sessions.delete_one({"secret": secret})
