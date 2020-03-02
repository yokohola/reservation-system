from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from room_service.serializers import RoomSerializer, ReservationSerializer
from room_service.models import Room, Reservation

__all__ = ['RoomCreateList', 'RoomRetrieveDestroy', 'ReservationCreateList']


class RoomCreateList(ListModelMixin,
                     CreateModelMixin,
                     GenericAPIView, ):
    """Get all rooms or create room"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RoomRetrieveDestroy(RetrieveDestroyAPIView):
    """Delete and retrieve room by primary key"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return super(RoomRetrieveDestroy, self).retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReservationCreateList(ListCreateAPIView):
    """Get all reservations or create reservation"""
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = (IsAuthenticated,)
