from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='fitbitlogin'),
    path('success', views.success, name='fitbitsuccess')
]