from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        token, username, password = request.POST.values()
        print(f'u:{username} p:{password}')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')

    return render(request, 'users/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):

    if request.method == 'POST':
        token, firstname, lastname, email, username, password, password_confirmation = request.POST.values()
        if password != password_confirmation:
            return render(request, 'users/signup.html', {'error': 'password does not match'})
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email,
                                        first_name=firstname,
                                        last_name=lastname)
        user.save()
        return redirect(request, 'login')
    return render(request, 'users/signup.html')
