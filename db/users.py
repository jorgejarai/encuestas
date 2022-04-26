from bcrypt import hashpw, gensalt, checkpw
from bson.objectid import ObjectId
from db import Singleton, Database


class Users(metaclass=Singleton):
    def get_all(self):
        ret = list(Database().pymongo.db.users.find())

        if ret:
            for user in ret:
                user.pop("password")
                user['_id'] = str(user['_id'])

        return ret

    def get_by_id(self, id):
        ret = Database().pymongo.db.users.find_one({"_id": ObjectId(id)})

        if ret:
            ret.pop("password")
            ret['_id'] = str(ret['_id'])

        return ret

    def get_by_email(self, email):
        ret = Database().pymongo.db.users.find_one({"email": email})

        if ret:
            ret.pop("password")
            ret['_id'] = str(ret['_id'])

        return ret

    def create(self, **kwargs):
        password = kwargs.pop("password")
        user = self.get_by_email(kwargs.get("email"))
        if user:
            return None

        kwargs["password"] = hashpw(password.encode(), gensalt())
        Database().pymongo.db.users.insert_one(kwargs)
        return kwargs

    def update(self, id, user):
        Database().pymongo.db.users.update_one({"_id": id}, {"$set": user})

    def delete(self, id):
        Database().pymongo.db.users.delete_one({"_id": id})

    def check_login(self, email, password):
        user = self.get_by_email(email)

        return checkpw(password, user.password)
