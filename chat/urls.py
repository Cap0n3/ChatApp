from django.urls import path
from .views import RoomListView, RoomView

urlpatterns = [
    path('', RoomListView.as_view(), name='room_list'),
    path('<str:room_name>/', RoomView.as_view(), name='room'),
]