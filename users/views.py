from django.shortcuts import render
from django.contrib.auth import authenticate, login

# Create your views here.


def user_login(request):

    return render(request, 'users/login.html')
