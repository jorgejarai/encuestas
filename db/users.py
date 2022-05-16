from bson.objectid import ObjectId
from db import Singleton, Database
import bcrypt


class Users(metaclass=Singleton):
    def get_all(self):
        """Obtiene una lista con todos los usuarios"""
        ret = list(Database().pymongo.db.users.find())

        if ret:
            for user in ret:
                user['_id'] = str(user['_id'])

        return ret

    def get_by_id(self, id: str):
        """Busca un usuario a partir de su ID. Retorna None si no lo encuentra"""
        ret = Database().pymongo.db.users.find_one({"_id": ObjectId(id)})

        if ret:
            ret['_id'] = str(ret['_id'])

        return ret

    def get_by_email(self, email: str):
        """Busca un usuario a partir de su email. Retorna None si no lo encuentra"""
        ret = Database().pymongo.db.users.find_one({"email": email})

        if ret:
            ret['_id'] = str(ret['_id'])

        return ret

    def create(self, **kwargs):
        """Crea un usuario a partir de **kwargs.

        Ejemplo: Users().create(name="Perico Pérez", email="perico@udec.cl",
                       role="respondent", interests=["male", "18-25", "biking",
                                                     "women", "programming"],
                       surveys=[])
        """

        user = self.get_by_email(kwargs.get("email"))
        if user:
            return None

        Database().pymongo.db.users.insert_one(kwargs)
        return kwargs

    def update(self, id: str, user: dict):
        """Actualiza los datos de un usuario con determinado ID

        Ejemplo: si tenemos un usuario con ID 1234 y correo "john@example.com",
            al que le queremos cambiar el correo a "doe.john@hello.org",
            podemos ejecutar

            Users().update("1234", {"email": "doe.john@hello.org"})

            Todos los demás atributos se conservan.
        """
        Database().pymongo.db.users.update_one(
            {"_id": ObjectId(id)}, {"$set": user})

    def delete(self, id: str):
        """Elimina los datos de un usuario con determinado ID"""
        Database().pymongo.db.users.delete_one({"_id": ObjectId(id)})

    def login(self, email: str, password: str):
        """Revisa si las credenciales del usuario dado son válidas"""

        user = self.get_by_email(email)

        if not user:
            return False

        return bcrypt.checkpw(password.encode(), user["password"].encode())
