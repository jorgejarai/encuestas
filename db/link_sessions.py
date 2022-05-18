from db import Singleton, Database
from datetime import datetime
from uuid import uuid4


class LinkSessions(metaclass=Singleton):
    def add(self, email: str):
        """Genera una sesión de link a la base de datos. Retorna un link
        de login automático para el usuario especificado."""

        secret = str(uuid4())

        Database().pymongo.db.link_sessions.insert_one({
            "email": email,
            "time": datetime.utcnow().timestamp(),
            "duration": 60 * 60 * 24 * 7,
            "secret": secret
        })

        return f"/login_link?secret={secret}"

    def check(self, secret: str):
        """Comprueba si un link de sesión es válido. Retorna True si es
        válido, False en caso contrario."""

        ret = Database().pymongo.db.link_sessions.find_one({"secret": secret})

        if not ret:
            return None

        Database().pymongo.db.link_sessions.delete_one({"secret": secret})

        if ret["time"] + ret["duration"] < datetime.utcnow().timestamp():
            return None

        return ret['email']
