from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    ListField,
    FloatField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ObjectIdField,
    BooleanField,
    PULL,
    IntField,
    DateTimeField,
    Q,
)
from mongoengine import signals
from datetime import datetime
from ..user.models import Requester, Tasker, User
import bson
from bson import Code, ObjectId, DBRef
from utils import convert_db_data_to_json, get_relevant_taskers, get_relevant_tasker


class Chat(EmbeddedDocument):
    message = StringField(required=True)
    response = StringField(required=True)
    is_final_outline = BooleanField(required=True)
    history = ListField()

class CodeChat(EmbeddedDocument):
    message = StringField(required=True)
    response = StringField(required=True)
    is_final_outline = BooleanField(required=True)
    history = ListField()


class Feedback(EmbeddedDocument):
    is_feedback = BooleanField(default=False)
    rate = FloatField(required=True, min_value=1, max_value=5)
    content = StringField()


class Submission(EmbeddedDocument):
    description = StringField()
    attachments = ListField(StringField(), default=[])
    date = DateTimeField()


class NewTask(Document):
    meta = {"collection": "tasks"}
    title = StringField(default="")
    description = StringField(default="")
    requester = ReferenceField(
        "User", default=None
    )  # Assuming `Requester` is another document
    worker = StringField(default="")
    cost = FloatField(default=0.0)
    status = StringField(choices=("todo", "doing", "review", "done"), default="todo")
    parent_id = StringField(default="")  # Default to None for root tasks
    sub_tasks_created = BooleanField(default=False)
    chat = ListField(EmbeddedDocumentField(Chat), default=list)
    code_chat = ListField(EmbeddedDocumentField(CodeChat), default=list)

    # addition information on Task
    workers = ListField(StringField(default=None), default=[])
    due_date = DateTimeField(default=None)
    priority = IntField(default=0)
    assignee = StringField(default=None)
    assigned_date = DateTimeField(default=None)
    labels = ListField(StringField(default=""), default=[])
    submission = EmbeddedDocumentField(Submission, default=None)
    tasker_feedback = EmbeddedDocumentField(Feedback, default=None)
    completed_date = DateTimeField(default=None)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.utcnow()

    # New method to set workers
    def set_workers(self, worker_ids):
        """
        Update the list of workers assigned to a task. This method can also include validation
        to check if worker IDs are valid if required.

        :param worker_ids: A list of worker IDs to be assigned to this task.
        """
        # Ensuring unique workers only
        unique_workers = set(worker_ids)

        # Optionally, add validation here to check each worker ID is valid

        # Update the workers list
        self.workers = list(unique_workers)
        self.save()  # Save the changes to the database

    @classmethod
    def find_task_by_id(cls, task_id):
        task = cls.objects(id=task_id).first()
        if not task:
            return None
        return task

    @classmethod
    def fetch_subtasks(cls, parent_id):
        tasks = cls.objects(parent_id=str(parent_id))
        subtask_list = []
        for task in tasks:
            subtask_data = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "worker": task.worker,
                "cost": task.cost,
                "status": task.status,
                "chat": task.chat,
                "code_chat": task.code_chat,
                "parent_id": str(task.parent_id) if task.parent_id else None,
                "submission": task.submission,
                "tasker_feedback": task.tasker_feedback,
                "due_date": task.due_date,
                "assigned_date": task.assigned_date,
                "priority": task.priority,
                "labels": task.labels,
                "completed_date": task.completed_date,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "tasks": cls.fetch_subtasks(task.id),  # Recursive call
            }

            if task.worker:
                assignee = User.objects.filter(id=task.worker).first()
                subtask_data["assignee"] = {
                    "id": assignee.id,
                    "name": assignee.name,
                    "avatar": assignee.avatar,
                }
            else:
                subtask_data["assignee"] = None
            subtask_list.append(subtask_data)
        return subtask_list

    @classmethod
    def find_task_by_id_expand(cls, task_id):
        """
        Retrieve a task by its ID, including all its subtasks and their subtasks recursively,
        with each task and subtask containing all relevant fields.
        """

        # Find the root task
        task = cls.objects(id=task_id).first()
        if not task:
            return None

        task_data = {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "worker": task.worker,
            "cost": task.cost,
            "status": task.status,
            "chat": task.chat,
            "code_chat": task.code_chat,
            "parent_id": str(task.parent_id) if task.parent_id else None,
            "submission": task.submission,
            "tasker_feedback": task.tasker_feedback,
            "sub_tasks_created": task.sub_tasks_created,
            "due_date": task.due_date,
            "assigned_date": task.assigned_date,
            "priority": task.priority,
            "labels": task.labels,
            "completed_date": task.completed_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "tasks": cls.fetch_subtasks(task.id),
        }

        if task.assignee:
            assignee = User.objects.filter(id=task.assignee).first()
            task_data["assignee"] = {
                "id": assignee.id,
                "name": assignee.name,
                "avatar": assignee.avatar,
            }
        else:
            assignee = None

        return task_data

    @classmethod
    def find_task_by_user(cls, user_id):
        # Fetch tasks directly assigned to the requester
        task_results = []
        root_tasks = cls.objects(Q(requester=user_id) & Q(parent_id="")).all()

        for task in root_tasks:
            # Attach subtasks dynamically
            if task["worker"]:
                task["worker"] = User.get_user_by_id(task["worker"])
            task_data = {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "worker": task.worker,
                "cost": task.cost,
                "status": task.status,
                "chat": task.chat,
                "code_chat": task.code_chat,
                "parent_id": str(task.parent_id) if task.parent_id else None,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "tasks": cls.fetch_subtasks(task.id),
            }
            task_results.append(task_data)
        return task_results

    @classmethod
    def insert_task(cls, task_data, parent_id=None, requester=""):
        """
        Recursively insert a task and its subtasks into the database.

        :param task_data: The dictionary containing task details.
        :param parent_id: The ID of the parent task. Default is None for top-level tasks.
        :return: None
        """
        # Create the task
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            # worker=task_data.get("worker", ""),  # Set to empty string if not specified
            cost=task_data.get("cost", 0.0),  # Set to 0.0 if not specified
            parent_id=str(parent_id),
            workers=get_relevant_taskers(),
            worker=get_relevant_tasker(),
            requester=requester,
        )
        new_task.save()

        # Check for subtasks and recursively insert them
        for subtask_data in task_data.get("sub_tasks", []):
            subtask = cls.insert_task(
                subtask_data, parent_id=new_task.id, requester=requester
            )

        new_task.save()  # Save again to update the sub_tasks field

        return new_task


# Registering the pre_save signal with NewTask
signals.pre_save.connect(NewTask.pre_save, sender=NewTask)
