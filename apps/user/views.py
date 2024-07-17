from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password, check_password

import json
import random
from bson import ObjectId

from .forms import (
    UserLoginForm,
    UserExistForm,
    UserRegisterationStep1Form,
    UserRegisterationStep2Form,
)

from .models import User
from utils import is_valid_solana_address, verify_signature, convert_db_data_to_json


@method_decorator(csrf_exempt, name="dispatch")
class SigninView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        form = UserLoginForm(data)

        if form.is_valid():
            public_key = data.get("public_key")
            request_nonce = data.get("request_nonce")
            signature = data.get("signature")
            wallet_type = data.get("wallet_type")

            # check to see if give public key is valid or not
            if is_valid_solana_address(public_key) == False:
                return JsonResponse(
                    {"message": "Invalid ${wallet_type} wallet address provided"},
                    safe=False,
                    status=400,
                )

            print("----", public_key, request_nonce, wallet_type)
            if request_nonce is True:
                # Generate a nonce (random number) between 10000 and 109998
                nonce = str(random.randint(10000, 109998))

                request.session["nonce"] = nonce
                return JsonResponse({"nonce": nonce}, safe=True, status=200)
            else:

                nonceToVerify = request.session["nonce"]
                print("publicKey", nonceToVerify, public_key, signature)
                verified = verify_signature(
                    nonceToVerify, signature, public_key, wallet_type
                )
                if verified == False:
                    return JsonResponse(
                        {"message": "Invalid signature, unable to login"},
                        safe=False,
                        status=400,
                    )

                user = User.get_by_solana_address(public_key)
                print(user)
                if user is None:
                    user = User.objects.create(**{f"{wallet_type}_address": public_key})
                user.nonce = nonceToVerify
                user.save()

                request.session["user_id"] = str(user.id)
                request.session["public_key"] = public_key
                request.session["logged"] = True

                print(request.session)

                return JsonResponse(
                    {
                        "message": "Logged in successfully",
                        "user": convert_db_data_to_json(user),
                    },
                    safe=True,
                    status=200,
                )

        else:
            return JsonResponse(
                {"message": "Invalid inputs", "errors": form.errors},
                safe=False,
                status=400,
            )


@method_decorator(csrf_exempt, name="dispatch")
class SignupView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        register_step = data.get("step")

        if register_step == "1":
            return handleRegisterStep1(data)
        elif register_step == "2":
            return handleRegisterStep2(data)


@method_decorator(csrf_exempt, name="dispatch")
class UserExist(View):
    def post(self, request):
        data = json.loads(request.body)
        form = UserExistForm(data)

        if form.is_valid():
            wallet_type = data.get("wallet_type")
            public_key = data.get("public_key")

            user = User.get_by_solana_address(public_key)

            if user is None:
                return JsonResponse({"exist": False, "message": "User Not Found"})
            else:
                # print (request.session, request.session["public_key"])
                if "public_key" in request.session:
                    return JsonResponse(
                        {
                            "exist": True,
                            "isAuthenticated": True,
                            "profile": convert_db_data_to_json(user),
                        },
                        status=200,
                    )
                return JsonResponse(
                    {
                        "exist": True,
                        "isAuthenticated": False,
                        "profile": convert_db_data_to_json(user),
                    },
                    status=200,
                )
        else:
            return JsonResponse({"message": "Invalid Request", "errors": form.errors})


def logout(request):
    if "logged" in request.session:
        del request.session["logged"]
        request.session.flush()  # Optional: Flush all of the session data
        return JsonResponse({"message": "You are logged out"}, safe=True, status=200)
    else:
        return JsonResponse(
            {"message": "You are already logged out"}, safe=False, status=400
        )


def handleRegisterStep1(data):
    form = UserRegisterationStep1Form(data)
    print("Tasker OnBoarding Process 1~~~")

    if form.is_valid():
        wallet_address = data.get("wallet_address")
        wallet_type = data.get("wallet_type")
        avatar = data.get("avatar")
        name = data.get("name")
        nation = data.get("nation")

        tasker = User.objects(**{f"{wallet_type}_address": wallet_address}).first()
        if tasker is None:
            return JsonResponse(
                {"message": "Tasker Not Found"},
                safe=False,
                status=400,
            )
        else:
            tasker.avatar = avatar
            tasker.name = name
            tasker.nation = nation
            tasker.register_step = "1"

            tasker.save()
            return JsonResponse(
                {"message": "Tasker OnBoarding Step 1 completed successfully"}
            )
    else:
        return JsonResponse(
            {"message": "Invalid inputs", "errors": form.errors},
            safe=False,
            status=400,
        )


def handleRegisterStep2(data):
    form = UserRegisterationStep2Form(data)
    print("Tasker OnBoarding Process 2~~~")

    if form.is_valid():
        wallet_address = data.get("wallet_address")
        wallet_type = data.get("wallet_type")
        skills = data.get("skills")
        desired_skills = data.get("desired_skills")

        tasker = User.objects(**{f"{wallet_type}_address": wallet_address}).first()
        if tasker is None:
            return JsonResponse(
                {"message": "Tasker Not Found"},
                safe=False,
                status=400,
            )
        else:
            tasker.skills = skills
            tasker.desired_skills = desired_skills
            tasker.register_step = "2"

            # Tasker Register Completed
            tasker.register_flag = True
            tasker.save()

            return JsonResponse(
                {"message": "Tasker OnBoarding Step 2 completed successfully"}
            )
    else:
        return JsonResponse(
            {"message": "Invalid inputs", "errors": form.errors},
            safe=False,
            status=400,
        )


@method_decorator(csrf_exempt, name="dispatch")
class UserByPublicKey(View):
    def get(self, request):
        wallet_type = request.GET.get("wallet_type", None)
        public_key = request.GET.get("public_key", None)

        user = User.objects(
            **{f"{wallet_type}_address": public_key},
        ).first()

        if user is None:
            return JsonResponse({"exist": False})

        return JsonResponse(
            {
                "exist": True,
                "role": "tasker" if user.register_flag else "requester",
                "user": convert_db_data_to_json(user),
            }
        )
