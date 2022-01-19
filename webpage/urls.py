"""webpage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

# Local
from main import views as main_views
from users import views as users_views


def root_url(request):
    return redirect('main')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(route='', view=root_url, name='root'),
    path(
        route='main/',
        view=main_views.main,
        name='main'),
    path(route='users/login/',
         view=users_views.user_login,
         name='login')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
