from rest_framework import serializers
from rest_framework.exceptions import ValidationError as RestValidationError
from django.core.exceptions import ValidationError as ModelsValidationError

from room_service.models import Room, Reservation
from room_service.validators import ReservationDateValidator

__all__ = ['ReservationSerializer', 'RoomSerializer']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'theme', 'room', 'date', 'start_time', 'end_time')

    def create(self, validated_data):
        try:
            return super(ReservationSerializer, self).create(validated_data)
        except ModelsValidationError as error:  # That is not good! Only for test
            raise RestValidationError(error.message)

    def validate(self, attrs):
        date = attrs.get('date')
        start = attrs.get('start_time')
        end = attrs.get('end_time')
        date_validator = ReservationDateValidator(date=date,
                                                  start=start,
                                                  end=end,
                                                  exc_class=RestValidationError)
        date_validator.validate()
        return super(ReservationSerializer, self).validate(attrs)


class RoomSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ('id', 'title', 'created_at', 'reservations',)
