from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from room_service.views import RoomCreateList, RoomRetrieveDestroy, ReservationCreateList

urlpatterns = [
    path('rooms/', RoomCreateList.as_view()),  # get/post
    path('rooms/<int:pk>/', RoomRetrieveDestroy.as_view()),  # get/delete
    path('reserve/', ReservationCreateList.as_view()),  # get, post
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', ])
