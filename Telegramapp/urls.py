from django.urls import path
from . import views

urlpatterns = [
    path('bot-view', views.bot_view, name='bot-view'),
]