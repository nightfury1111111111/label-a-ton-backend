from django.urls import path
from .views import (
    create_task,
    go_chat,
    go_code_chat,
    get_task,
    update_task,
    get_task_by_user,
    get_tasks,
    get_requests,
    get_board_requests,
    get_request,
    assign_tasker,
    submit_result,
    approve_task,
    approve_task_by_AI,
    leave_feedback,
    reject_task,
    save_chat,
    save_code_chat
)

urlpatterns = [
    path("", create_task, name="create-task"),
    path("all/", get_tasks, name="get-tasks"),
    path("addToBoard/", assign_tasker, name="assign-tasker"),
    path("submit/", submit_result, name="submit-result"),
    path("getRequests/", get_requests, name="get-requests"),
    path("getBoardRequests/", get_board_requests, name="get-board-requests"),
    path("getTaskByUser/", get_task_by_user),
    path("getRequest/<str:taskId>", get_request, name="get-request-tasker"),
    path("updateTask/<str:taskId>/", update_task),
    path("approveTask/", approve_task),
    path("approveTaskByAI/", approve_task_by_AI),
    path("rejectTask/", reject_task),
    path("leaveFeedback/", leave_feedback),
    path("<str:taskId>/chat/", go_chat),
    path("<str:taskId>/code_chat/", go_code_chat),
    path("<str:taskId>/", get_task),
    path("subtask/chat/<str:taskId>/", save_chat),
    path("subtask/code_chat/<str:taskId>/", save_code_chat),
]
