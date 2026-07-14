from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_page, name='chatbot_page'),
    path('response/', views.chatbot_response, name='chatbot_response'),
]
