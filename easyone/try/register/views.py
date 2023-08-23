from collections import UserDict
from typing import Counter
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.
from django.http.response import JsonResponse
from register.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, QueryDict
from django.contrib import auth
from django.contrib.sessions.models import Session
# from register.forms import *
import time
# from .forms import RegisterForm
from django.core import serializers
from django.core.mail import EmailMessage, message
from django.utils import timezone
import random
import urllib.parse
import json
import re


@csrf_exempt#我要拿來增加cpu使用量啦JOJO!
def Shock(request):
    if request.method == 'POST':
        status = "0"
        status = "2"
        current_time = time.time() # 當下時間的 Unix timestamp
        seconds_sum = sum(int(d) for d in str(int(current_time))) # 所有位數的數字加總
        squared_sum = seconds_sum ** 2 # 加總後的數字平方
        strs=(str(squared_sum)+"\n")
        with open('aaa.txt', 'a') as f:
            f.write(strs)
        return JsonResponse({"status":status,"math":str(squared_sum),'name':(current_time)})
    else:
        status = "1"
        return JsonResponse({"status":status})