from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

from room_service.validators import ReservationDateValidator

__all__ = ["Room", "Reservation"]


class Room(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Reservation(models.Model):
    theme = models.CharField(max_length=128, blank=False, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    date = models.DateField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)

    def __str__(self):
        return self.theme

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.clean()
        return super(Reservation, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def clean(self):
        validator = ReservationDateValidator(self.date,
                                             self.start_time,
                                             self.end_time,
                                             ValidationError)
        validator.validate()
        self.check_reservation_unique()

    def check_reservation_unique(self):
        if (
            Reservation.objects.filter(
                room_id=self.room.id, date=self.date, start_time=self.start_time
            )
            | Reservation.objects.filter(
                room_id=self.room.id, date=self.date, end_time=self.end_time
            )
            | Reservation.objects.filter(
                room_id=self.room,
                date=self.date,
                start_time__lt=self.start_time,
                end_time__gt=self.start_time,
            )
            | Reservation.objects.filter(
                room_id=self.room,
                date=self.date,
                start_time__lt=self.end_time,
                end_time__gt=self.end_time,
            )
            | Reservation.objects.filter(
                room_id=self.room,
                date=self.date,
                start_time__gt=self.start_time,
                end_time__lt=self.end_time,
            )
        ).exists():
            msg = "Room number `{}` is already reserved for the date `{}`, `{}` to `{}`".format(
                self.room.id, self.date, self.start_time, self.end_time
            )
            raise ValidationError(msg)
