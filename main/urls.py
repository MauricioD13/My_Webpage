from django.urls import path
from . import views

urlpatterns = [
    path(
        route='main/',
        view=views.main,
        name='main'),
]
