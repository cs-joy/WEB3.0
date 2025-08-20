from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.ask_question, name='ask_question'),
    path('history/<str:user_address>/', views.get_chat_history, name='get_chat_history'),
    path('blockchain-history/<str:user_address>/', views.get_blockchain_history, name='get_blockchain_history'),
]
