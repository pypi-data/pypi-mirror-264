from typing import Dict, List
from pymongo import MongoClient
from bson import ObjectId

from taskcrow.status import Status
from taskcrow.task_category import TaskCategory

from .task import Task
from .utils.uuid import generate_uuid_from_seed



def get_taskout_collection_name(task_type: str):
    return f"TASKOUT__{task_type}"

def get_task_collection_name(task_type: str):
    return f"TASK__{task_type}"

def generate_task_id(task_type:str, unique_id:str):
    task_id = str(generate_uuid_from_seed(f'{task_type}_{unique_id}'))
    return task_id


class TaskCoordinate:
    DATABASE_NAME_TEMPLATE = 'task_db__{category_name}_{category_value}'

    def __init__(self,
                 *,
                 dsn,
                 category_name,
                 category_value,
                 ):
        self.client = MongoClient(dsn)
        self.db = None
        self.task_category_name = category_name
        self.task_category_value = category_value

        # 입력받은 Argument를 이용해 추가적인 초기화 작업 수행
        self._select_database()

    def set_task_category(self, category_name: str, category_value:str):
        self.task_category_name = category_name
        self.task_category_value = category_value

    def _make_database_name(self):
        database_name = self.DATABASE_NAME_TEMPLATE.format(
            category_name=self.task_category_name,
            category_value=self.task_category_value)
        return database_name

    def _select_database(self):
        database_name = self._make_database_name()
        self.db = self.client[database_name]

    def create_task(self,
                    task:Task
                    ):
        task_type = task.task_type
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        if task.id is None:
            task.id = ObjectId()
        inserted_id = self.db[collection].insert_one(vars(task)).inserted_id
        return inserted_id

    def create_task_output(self,
                    task:Task
                    ):
        task_type = task.task_type
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = get_task_collection_name(task_type)
        if task.id is None:
            task.id = ObjectId()
        inserted_id = self.db[collection].insert_one(vars(task)).inserted_id
        return inserted_id

    def is_task_duplicate(self,task_type, id: str):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = get_task_collection_name(task_type)
        is_duplicate = self.db[collection].find_one({'_id': id})
        return is_duplicate

    def count_tasks(self, task_type, query):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = get_task_collection_name(task_type)
        counts = self.db[collection].count_documents(query)
        return counts

    def find_tasks(self, task_type, query, limit=10, skip=0):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = get_task_collection_name(task_type)
        tasks = self.db[collection].find(query).limit(limit).skip(skip)
        # return [Task(self.db, task_id=str(task['_id']), **task) for task in tasks]
        return [Task(
                     id=str(task.get('_id')) or None,
                     sub_ids=task.get('sub_ids') or None,
                     task_type=task.get('type') or None,
                     parameters=task.get('parameters') or None,
                     status=task.get('status') or None,
                     lineage=task.get('lineage') or None,
                     result=task.get('result') or None,
                     created_at=task.get('created_at') or None,
                     updated_at=task.get('updated_at') or None
                    ) for task in tasks]

    def find(self, task_type, query):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        tasks_cursor = self.db[collection].find(query)
        for task in tasks_cursor:
            yield Task(
                        id=str(task.get('_id')),
                        sub_ids=task.get("sub_ids") or None,
                        task_type=task.get('type'),
                        parameters=task.get('parameters'),
                        status=task.get('status'),
                        lineage=task.get('lineage') or None,
                        result=task.get('result'),
                        created_at=task.get('created_at') or None,
                        updated_at=task.get('updated_at') or None
                        )

    def find_one_and_update(self, task_type, query, update, return_document=True):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = get_task_collection_name(task_type)
        task = self.db[collection].find_one_and_update(query, update, return_document=return_document)
        # return [Task(self.db, task_id=str(task['_id']), **task) for task in tasks]
        return Task(
                    id=str(task.get('_id')),
                    sub_ids=task.get("sub_ids") or None,
                    task_type=task.get('type'),
                    parameters=task.get('parameters'),
                    status=task.get('status'),
                    lineage=task.get('lineage') or None,
                    result=task.get('result'),
                    created_at=task.get('created_at') or None,
                    updated_at=task.get('updated_at') or None
                    )


    def get_task(self, task_type, task_id):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = get_task_collection_name(task_type)
        task = self.db[collection].find_one({"_id": ObjectId(task_id)})
        if task is None:
            return None
        return Task(
                    id=str(task.get('_id')),
                    sub_ids=task.get("sub_ids") or None,
                    task_type=task.get('type'),
                    parameters=task.get('parameters'),
                    status=task.get('status'),
                    lineage=task.get('lineage') or None,
                    result=task.get('result'),
                    created_at=task.get('created_at') or None,
                    updated_at=task.get('updated_at') or None
                )

    def get_collection_name(self, task:Task)->str:
        if self.task_category_name == str(TaskCategory.GRID).lower():
            return get_task_collection_name(task.task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            return get_taskout_collection_name(task.task_type)

    def collection_names(self):
        return self.db.list_collection_names()


    def delete_one(self, task: Task):
        task_type = task.task_type
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        return self.db[collection].delete_one({'_id': task.id})


    def delete_many(self, task_type:str, query): # type: ignore
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        return self.db[collection].delete_many(query)

    def delete_many_by_tasks(self, tasks: List[Task]): # type: ignore
        groups = self._group_tasks_by_type(tasks)
        for task_type, tasks in enumerate(groups):
            ids = map(lambda x:x.id, tasks)

            if self.task_category_name == str(TaskCategory.GRID).lower():
                collection = get_task_collection_name(task_type)
            elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
                collection = get_taskout_collection_name(task_type)

            # collection = self.get_task_collection_name(task_type)
            self.db[collection].update_one({'_id':{'$in': ids}})
        return None

    def _group_tasks_by_type(tasks)-> Dict[str, List[Task]]:
        grouped_tasks = {}
        for task in tasks:
            # 해당 task_type의 리스트가 이미 딕셔너리에 있으면 해당 리스트에 id 추가
            # 없으면 새로운 리스트를 생성하여 딕셔너리에 추가
            if task.task_type in grouped_tasks:
                grouped_tasks[task.task_type].append(task)
                # grouped_tasks[task.task_type].append(task.id)
            else:
                grouped_tasks[task.task_type] = [task]
                # grouped_tasks[task.task_type] = [task.id]
        return grouped_tasks

    def update_one_by_task(self, task: Task):
        task_type = task.task_type
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = self.get_task_collection_name(task_type)
        try:
            self.db[collection].update_one({'_id':ObjectId(task.id)}, vars(task))
        except Exception as e:
            self.db[collection].update_one({'_id':task.id}, vars(task))



    def update_many(self, task_type:str, query, update):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = self.get_task_collection_name(task_type)
        self.db[collection].update_many(query, update)


    def update_many_by_tasks(self, tasks: List[Task]):
        for task in tasks:
            self.update_one_by_task(task)

    def update_status(self, task: Task, task_type:str, status: Status, result=None):
        if self.task_category_name == str(TaskCategory.GRID).lower():
            collection = get_task_collection_name(task_type)
        elif self.task_category_name == str(TaskCategory.OUTPUT).lower():
            collection = get_taskout_collection_name(task_type)
        # collection = self.get_task_collection_name(task_type)
        try:
            self.db[collection].update_one({'_id':ObjectId(task.id)}, {'$set':{'status': status, 'result':result}})
        except Exception as e:
            self.db[collection].update_one({'_id':task.id}, {'$set':{'status': status, 'result':result}})

