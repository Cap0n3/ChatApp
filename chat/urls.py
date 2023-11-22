from django.urls import path
from .views import IndexView, RoomListView, RoomView

urlpatterns = [
    path('home/', IndexView.as_view(), name='index'),
    path('', RoomListView.as_view(), name='room_list'),
    path('<str:room_name>/', RoomView.as_view(), name='room'),
]