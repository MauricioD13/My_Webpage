from django.urls import path
from . import views

urlpatterns = [
    path(route='login/',
         view=views.user_login,
         name='login'),
    path(route='logout/',
         view=views.logout_view,
         name='logout'),
    path(route='signup/',
         view=views.signup_view,
         name='signup')
]
