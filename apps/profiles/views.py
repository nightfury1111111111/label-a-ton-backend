from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..user.models import Requester, Tasker, User
from ..tasks.models import NewTask
from bson import ObjectId
from utils.utils import convert_db_data_to_json
import json


@api_view(["GET"])
def get_profile(request, id):
    user = User.objects(id=id).first()
    if user is None:
        return JsonResponse({"message": "User not found"}, status=400)

    feedbacks = []
    for feedback in user.feedbacks:
        task = NewTask.find_task_by_id(task_id=str(feedback.task_id))
        feedback = {
            "task_id": str(task.id),
            "title": task.title,
            "description": task.description,
            "cost": task.cost,
            "dueDate": task.due_date,
            "completedDate": task.completed_date,
            "isFeedback": feedback.is_feedback,
            "content": feedback.content,
            "rate": feedback.rate,
        }
        feedbacks.append(feedback)

    user_dict = {
        "_id": str(user.id),
        "registerFlag": user.register_flag,
        "name": user.name,
        "avatar": user.avatar,
        "nation": user.nation,
        "isDaoMember": user.is_dao_member,
        "skills": user.skills,
        "desiredSkills": user.desired_skills,
        "agents": user.agents,
        "workHistory": user.work_history,
        "totalEarnings": user.total_earnings,
        "totalJobs": user.total_jobs,
        "hourlyRate": user.hourly_rate,
        "rejectedJobs": user.rejected_jobs,
        "feedbacks": feedbacks,
    }

    return Response(user_dict, status=200)


# Create your views here.
@api_view(["POST"])
def update_profile(request):
    # get user id here(will be changed accordingly) from session
    userId = request.session.get("user_id")

    requester = Requester.objects(id=userId).first()
    tasker = Tasker.objects(id=userId).first()

    user = Requester.objects(id=userId).first()

    if user is None:
        return JsonResponse({"message": "Invalid request, User not found"}, status=400)

    for key, value in request.data.items():
        # Skip 'userId' key as it's not a field of Tasker
        if key != "userId" and key != "role":
            setattr(user, key, value)

    # Save the updated user object
    user.save()
    user_dict = user.to_mongo().to_dict()
    for key, value in user_dict.items():
        if isinstance(value, ObjectId):
            user_dict[key] = str(value)

    return Response(user_dict, status=200)
