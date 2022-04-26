from bson.objectid import ObjectId
from db import Singleton, Database


class Surveys(metaclass=Singleton):
    def get_all(self):
        ret = list(Database().pymongo.db.surveys.find())

        if ret:
            for survey in ret:
                survey['_id'] = str(survey['_id'])

        return ret

    def get_by_id(self, id):
        ret = Database().pymongo.db.surveys.find_one({"_id": ObjectId(id)})

        if ret:
            ret['_id'] = str(ret['_id'])

        return ret

    def create(self, **kwargs):
        return kwargs

    def update(self, id, survey):
        Database().pymongo.db.surveys.update_one({"_id": id}, {"$set": survey})

    def delete(self, id):
        Database().pymongo.db.surveys.delete_one({"_id": id})
