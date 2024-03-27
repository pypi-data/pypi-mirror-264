from datetime import datetime
from enum import Enum
from pymongo import MongoClient
from bson import ObjectId

from taskcrow.exception import DataNotInsertedError
from taskcrow.status import Status


class Task:
    def __init__(self,
                 *,
                 id=None,
                 sub_ids=None,
                 task_type=None,
                 parameters=None,
                 status=Status.PENDING,
                 result=None,
                 lineage=[],
                 created_at=None,
                 updated_at=None

                 ):
        self.id = id
        self.sub_ids = sub_ids
        self.task_type = task_type
        self.parameters = parameters
        self.status = status
        self.lineage = lineage or []
        self.result = result
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()


    def set_task_id(self, task_id:str):
        self.sub_ids['task_id'] = task_id

    def inherit_lineage(self, parent_task):
        if parent_task.lineage:
            self.lineage.extend(parent_task.lineage)
        self.lineage.append(parent_task.task_id)

    # def save(self):
    #     task_data = {
    #         "_id": ObjectId(),
    #         "sub_ids": {'task_id':self.task_id},
    #         "type": self.task_type,
    #         "parameters": self.parameters,
    #         "status": Status.PENDING,
    #         "result": self.result,
    #         "lineage": self.lineage,
    #         "created_at": datetime.now(),
    #         "updated_at": datetime.now()
    #     }

    #     return self.db.tasks.insert_one(task_data).inserted_id

    # def insert(self, status, result=None):
    #     self.status = status
    #     self.result = result
    #     inserted_id = self.db.tasks.insert_one(
    #         # {"_id": ObjectId(self.task_id)},
    #         {"_id": self.task_id},
    #         {"$set": {"status": status, "result": result}}
    #     )
    #     self.id = inserted_id

    #     return inserted_id

    # def update(self, status, result=None):
    #     if self.id is None:
    #         raise DataNotInsertedError()
    #     self.status = status
    #     self.result = result
    #     return self.db.tasks.update_one(
    #         {"_id": self.id},
    #         {"$set": {"status": status, "result": result}}
    #     )



    # def delete(self):
    #     return self.db.tasks.delete_one({"_id": ObjectId(self.task_id)})