from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Chat, NewTask, Submission, Feedback, CodeChat
from ..user.models import Feedback as Feedback_User
from ..user.models import User
from .serializers import TaskSerializer
from django.conf import settings
import os
import json
import requests
from .forms import ChatForm, SubmissionForm, FeedbackForm
from bson import ObjectId
from mongoengine import Document, EmbeddedDocument
import datetime
from django.views.decorators.csrf import csrf_exempt
from utils import convert_db_data_to_json, get_relevant_taskers


def convertDBDataToJson(data):
    if isinstance(data, (Document, EmbeddedDocument)):
        data = data.to_mongo()  # Convert document to a MongoDB dict

    if isinstance(data, dict):
        return {
            k: convertDBDataToJson(v) for k, v in data.items()
        }  # Optionally exclude '_id'
    elif isinstance(data, list):
        return [convertDBDataToJson(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    else:
        return data


def mapTasks(task, fields_to_include=None):
    if fields_to_include is None:
        # If fields_to_include is None, include all fields
        return {key: value for key, value in task.items()}
    else:
        # Only include specified fields
        return {field: task[field] for field in fields_to_include if field in task}


@api_view(["GET"])
def get_tasks(request):
    tasks = NewTask.objects.all()
    tasks = [convert_db_data_to_json(task) for task in tasks]
    tasks = [
        mapTasks(
            task,
            fields_to_include=[
                "id",
                "parentId",
                "title",
                "description",
                "requester",
                "worker",
                "cost",
                "status",
                "createdAt",
                "updatedAt",
            ],
        )
        for task in tasks
    ]
    for task in tasks:
        # Check if 'requester' key exists and is not None
        if task.get("requester"):
            # Fetch the 'requester' user and convert it to JSON
            requester_user = User.objects.filter(id=str(task["requester"])).first()
            if requester_user:
                task["requester"] = mapTasks(
                    convert_db_data_to_json(requester_user),
                    fields_to_include=["id", "name", "avatar"],
                )
            else:
                task["requester"] = (
                    None  # Ensure that there is always a requester key, even if it's None
                )

    return Response({"tasks": tasks}, status=200)


@api_view(["GET"])
def get_requests(request):
    tasks = NewTask.objects(
        workers__contains=str(request.session.get("user_id")), assignee=None
    )  # we have to do it by session
    tasks = [convert_db_data_to_json(task) for task in tasks]
    tasks = [
        mapTasks(
            task,
            fields_to_include=[
                "id",
                "parentId",
                "title",
                "description",
                "requester",
                "workers",
                "priority",
                "cost",
                "status",
                "assignee",
                "createdAt",
                "updatedAt",
            ],
        )
        for task in tasks
    ]
    for task in tasks:
        # Check if 'requester' key exists and is not None
        if task.get("requester"):
            # Fetch the 'requester' user and convert it to JSON
            requester_user = User.objects.filter(id=str(task["requester"])).first()
            if requester_user:
                task["requester"] = mapTasks(
                    convert_db_data_to_json(requester_user),
                    fields_to_include=["id", "name", "avatar"],
                )
            else:
                task["requester"] = (
                    None  # Ensure that there is always a requester key, even if it's None
                )

    return Response({"tasks": tasks}, status=200)


@api_view(["GET"])
def get_board_requests(request):
    user_id = request.session.get("user_id")
    print(user_id)
    tasks = NewTask.objects(
        assignee=user_id,  # This specifies that assignee should not be None
    )

    tasks = [convert_db_data_to_json(task) for task in tasks]
    tasks = [
        mapTasks(
            task,
            fields_to_include=[
                "id",
                "parentId",
                "title",
                "description",
                "requester",
                "priority",
                "workers",
                "cost",
                "status",
                "assignee",
                "createdAt",
                "submission",
                "taskerFeedback",
                "updatedAt",
            ],
        )
        for task in tasks
    ]
    for task in tasks:
        # Check if 'requester' key exists and is not None
        if task.get("requester"):
            # Fetch the 'requester' user and convert it to JSON
            requester_user = User.objects.filter(id=str(task["requester"])).first()
            if requester_user:
                task["requester"] = mapTasks(
                    convert_db_data_to_json(requester_user),
                    fields_to_include=["id", "name", "avatar"],
                )
            else:
                task["requester"] = (
                    None  # Ensure that there is always a requester key, even if it's None
                )
    return Response({"tasks": tasks}, status=200)


@api_view(["POST"])
def create_task(request):
    userId = request.session.get("user_id")
    task = NewTask(requester=userId).save()

    return Response({"taskId": str(task.id)}, status=201)


@api_view(["GET"])
def get_task(request, taskId):
    task = NewTask.find_task_by_id_expand(task_id=taskId)
    print(">>>>>>>>>>>>>>>>>>>>>>>Request is arrived", task["worker"])

    if task is None:
        return Response({"message": "Task not found."}, status=400)

    if task["worker"]:
        worker_data = User.get_user_by_id(task["worker"])
        print("worker", worker_data)
        if worker_data:
            task["worker"] = {
                "id": str(worker_data.id),
                "name": worker_data.name,
                "solana_address": worker_data.solana_address,
                "avatar_url": worker_data.avatar,
                # Include other fields as needed
            }
        else:
            task["worker"] = None
    
    return Response(convertDBDataToJson(task), status=200)


@api_view(["GET"])
def get_request(request, taskId):
    task = NewTask.find_task_by_id(task_id=taskId)
    user_id = request.session.get("user_id")

    if task is None:
        return Response({"message": "Task not found."}, status=400)
    # if task.assignee is not None or user_id not in task.workers:
    #     return Response({"message": "Permission not allowed."}, status=400)

    task_dict = convertDBDataToJson(task)
    requester = convertDBDataToJson(task.requester)
    print(requester)
    task_dict["requester"] = {
        "id": requester["_id"],
        "name": requester["name"],
        "avatar": requester["avatar"],
    }

    return Response(task_dict, status=200)


@api_view(["POST"])
def assign_tasker(request):
    data = json.loads(request.body)
    user_id = request.session.get("user_id")

    task_id = data.get("task_id")
    task = NewTask.find_task_by_id(task_id=task_id)

    if task is None:
        return Response({"message": "Task not found."}, status=400)
    if task.assignee is not None or user_id not in task.workers:
        return Response({"message": "Permission not allowed."}, status=400)

    task.assignee = user_id
    task.assigned_date = datetime.datetime.now()
    task.status = "doing"
    task.save()

    task_dict = convertDBDataToJson(task)
    requester = convertDBDataToJson(task.requester)
    task_dict["requester"] = {
        "id": requester["_id"],
        "name": requester["name"],
        "avatar": requester["avatar"],
    }
    return Response(task_dict, status=200)


@api_view(["POST"])
def submit_result(request):
    data = json.loads(request.body)
    form = SubmissionForm(data)

    if form.is_valid():
        user_id = request.session.get("user_id")

        task_id = data.get("task_id")
        description = data.get("description")
        upload_paths = data.get("upload_paths")
        task = NewTask.find_task_by_id(task_id=task_id)

        if task is None:
            return Response({"message": "Task not found."}, status=400)

        print(task.assignee, "----", user_id)
        if str(task.assignee) != user_id:
            return Response({"message": "Permission not allowed."}, status=400)

        submission = Submission(
            description=description,
            attachments=upload_paths,
            date=datetime.datetime.now(),
        )
        task.submission = submission
        task.status = "review"
        task.save()

        task_dict = convertDBDataToJson(task)
        requester = convertDBDataToJson(task.requester)
        task_dict["requester"] = {
            "id": requester["_id"],
            "name": requester["name"],
            "avatar": requester["avatar"],
        }
        return Response(task_dict, status=200)
    else:
        return Response(
            {"message": "Invalid inputs", "errors": form.errors}, status=400
        )


@api_view(["POST"])
def approve_task(request):
    data = json.loads(request.body)
    user_id = request.session.get("user_id")

    task_id = data.get("task_id")
    task = NewTask.find_task_by_id(task_id=task_id)

    if task is None:
        return Response({"message": "Task not found."}, status=400)
    if str(task.requester.id) != user_id:
        return Response({"message": "Permission not allowed."}, status=400)
    if task.status == "done":
        return Response({"message": "Task has already done."}, status=400)
    
    if(data.get("tasker") == "OpenAI"):
        task.complete_by_AI = True
        task.status = "done"
        task.completed_date = datetime.datetime.now()
        return Response(convertDBDataToJson(task), status=200)

    if task.submission is None:
       return Response({"message": "No submission."}, status=400)
    
    task.status = "done"
    task.completed_date = datetime.datetime.now()
    task.save()

    # update tasker
    tasker = User.objects.filter(id=str(task.assignee)).first()
    tasker.total_earnings += task.cost if task.cost else 0
    tasker.total_jobs += 1
    tasker.save()

    task_data = convertDBDataToJson(task)
    assignee = User.objects.filter(id=task.assignee).first()
    task_data["assignee"] = {
        "id": str(assignee.id),
        "name": assignee.name,
        "avatar": assignee.avatar,
    }

    return Response(task_data, status=200)


@api_view(["POST"])
def approve_task_by_AI(request):
    data = json.loads(request.body)
    task_id = data.get("task_id")
    task = NewTask.find_task_by_id(task_id=task_id)

    if task is None:
        return Response({"message": "Task not found."}, status=400)
    if task.status == "done":
        return Response({"message": "Task has already done."}, status=400)
    
    task.complete_by_AI = True
    task.status = "done"
    submission = Submission(
        description = data.get("description"),
        attachments = data.get("upload_paths"),
        date = datetime.datetime.now(),
    )
    task.submission = submission
    task.completed_date = datetime.datetime.now()
    task.save()
    return Response(convertDBDataToJson(task), status=200)


@api_view(["POST"])
def reject_task(request):
    data = json.loads(request.body)
    user_id = request.session.get("user_id")

    task_id = data.get("task_id")
    task = NewTask.find_task_by_id(task_id=task_id)

    if task is None:
        return Response({"message": "Task not found."}, status=400)
    if str(task.requester.id) != user_id:
        return Response({"message": "Permission not allowed."}, status=400)
    if task.status != "review":
        return Response(
            {"message": "Task status is not valid for this operation."}, status=400
        )
    if task.submission is None:
        return Response({"message": "No submission."}, status=400)

    task.status = "todo"
    task.assignee = None
    task.assigned_date = None
    task.submission = None
    task.save()

    task_data = convertDBDataToJson(task)
    return Response(task_data, status=200)


@api_view(["POST"])
def leave_feedback(request):
    data = json.loads(request.body)
    form = FeedbackForm(data)

    if form.is_valid():
        user_id = request.session.get("user_id")

        task_id = data.get("task_id")
        is_feedback = data.get("is_feedback")
        content = data.get("content")
        rate = data.get("rate")
        task = NewTask.find_task_by_id(task_id=task_id)

        if task is None:
            return Response({"message": "Task not found."}, status=400)

        if str(task.requester.id) != user_id:
            return Response({"message": "Permission not allowed."}, status=400)

        # add feeback to task
        feedback = Feedback(is_feedback=is_feedback, content=content, rate=rate)
        task.tasker_feedback = feedback
        task.save()

        # add feedback to
        if is_feedback:
            user = User.objects.filter(id=str(task.requester.id)).first()
            feedback = Feedback_User(
                task_id=task_id, is_feedback=is_feedback, content=content, rate=rate
            )
            user.feedbacks.append(feedback)
            user.save()

        return Response(convertDBDataToJson(task), status=200)
    else:
        return Response(
            {"message": "Invalid inputs", "errors": form.errors}, status=400
        )


@api_view(["POST"])
def get_task_by_user(request):
    data = json.loads(request.body)
    is_all = data.get("is_all")
    fields = data.get("fields")

    print(is_all, fields)

    user_id = request.session.get("user_id")
    tasks = NewTask.find_task_by_user(user_id)
    tasks = [convertDBDataToJson(task) for task in tasks]
    if is_all is False:
        tasks = [mapTasks(task, fields_to_include=fields) for task in tasks]

    return Response({"tasks": tasks}, status=200)


@api_view(["POST"])
def update_task(request, taskId):
    task = NewTask.find_task_by_id(task_id=taskId)
    if task is None:
        return Response({"message": "Task not found."}, status=400)

    data = json.loads(request.body)
    print("update task", data)
    for key, value in data.items():
        print(key, value)
        task[key] = value
    task.save()

    return Response({"task": convertDBDataToJson(task), "success": True}, status=200)


@api_view(["POST"])
def go_chat(request, taskId):
    data = json.loads(request.body)
    form = ChatForm(data)

    user_id = request.session.get("user_id")

    if form.is_valid():
        message = data.get("message")
        history = data.get("history")

        task_id = taskId
        print(task_id, message, history)

        task = NewTask.find_task_by_id(task_id=task_id)
        if task is None:
            return Response({"message": "Task Not Found"}, status=400)

        # get ai reponse from openai-server
        response = requests.post(
            os.getenv("OPENAI_CHAT_SERVER_URL"),
            json={"message": message, "history": history},
        )

        response = response.json()

        print(response, response["response"])

        if "title" in response:
            task.title = response.title

        # add chat
        chat = Chat(
            message=message,
            response=response["response"],
            history=response["history"],
            is_final_outline=response["is_final_outline"],
        )
        task.chat.append(chat)
        task.save()

        # create sub tasks if sub_tasks_created is False
        if response["is_final_outline"] is True and task.sub_tasks_created is False:
            # print('---Start:',datetime.datetime.now())
            for task_data in response["final_outline"]["main_tasks"]:
                new_task = NewTask.insert_task(task_data, task.id, user_id)
            # print('---Fetched:',datetime.datetime.now())

            task.sub_tasks_created = True
            task.save()
            # print('---Saved:',datetime.datetime.now())

            tasks = NewTask.find_task_by_id_expand(task.id)["tasks"]
            # if sub tasks created, add to response
            result = [convertDBDataToJson(task) for task in tasks]
            response["tasks"] = result

        print("message, history", response)
        return Response(response, status=200)
    else:
        return Response(
            {"message": "Invalid inputs", "errors": form.errors}, status=400
        )
    
@api_view(["POST"])
def go_code_chat(request, taskId):
    data = json.loads(request.body)
    form = ChatForm(data)

    user_id = request.session.get("user_id")

    if form.is_valid():
        message = data.get("message")
        history = data.get("history")

        task_id = taskId
        print(task_id, message, history)

        task = NewTask.find_task_by_id(task_id=task_id)
        if task is None:
            return Response({"message": "Task Not Found"}, status=400)

        # get ai reponse from openai-server
        response = requests.post(
            os.getenv("OPENAI_CHAT_SERVER_URL"),
            json={"message": message, "history": history},
        )

        response = response.json()

        print(response, response["response"])

        if "title" in response:
            task.title = response.title

        # add chat
        chat = CodeChat(
            message=message,
            response=response["response"],
            history=response["history"],
            is_final_outline=response["is_final_outline"],
        )
        task.code_chat.append(chat)
        task.save()

        # create sub tasks if sub_tasks_created is False
        if response["is_final_outline"] is True and task.sub_tasks_created is False:
            # print('---Start:',datetime.datetime.now())
            for task_data in response["final_outline"]["main_tasks"]:
                new_task = NewTask.insert_task(task_data, task.id, user_id)
            # print('---Fetched:',datetime.datetime.now())

            task.sub_tasks_created = True
            task.save()
            # print('---Saved:',datetime.datetime.now())

            tasks = NewTask.find_task_by_id_expand(task.id)["tasks"]
            # if sub tasks created, add to response
            result = [convertDBDataToJson(task) for task in tasks]
            response["tasks"] = result

        print("message, history", response)
        return Response(response, status=200)
    else:
        return Response(
            {"message": "Invalid inputs", "errors": form.errors}, status=400
        )


@api_view(["POST"])
def save_chat(request, taskId):
    task = NewTask.find_task_by_id(task_id=taskId)
    if task is None:
        return Response({"message": "Task not found."}, status=400)

    data = json.loads(request.body)
    # Load existing chat data
    chat = Chat(
            message=data["message"],
            response=data["response"],
            history=data["history"],
            is_final_outline=False
        )
    task.chat.append(chat)
    task.save()
    # return Response(status=200, {"task": task, "success":True})
    return Response({"task": convertDBDataToJson(task), "success": True}, status=200)
    # for key, value in data.items():
    #     print(key, value)
    #     task[key] = value
    # task.save()

    # return Response({"task": convertDBDataToJson(task), "success": True}, status=200)

@api_view(["POST"])
def save_code_chat(request, taskId):
    task = NewTask.find_task_by_id(task_id=taskId)
    if task is None:
        return Response({"message": "Task not found."}, status=400)

    data = json.loads(request.body)
    # Load existing chat data
    chat = CodeChat(
            message=data["message"],
            response=data["response"],
            history=data["history"],
            is_final_outline=False
        )
    task.code_chat.append(chat)
    task.save()
    # return Response(status=200, {"task": task, "success":True})
    return Response({"task": convertDBDataToJson(task), "success": True}, status=200)