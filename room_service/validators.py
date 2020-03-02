from datetime import datetime, time as t
from django.utils import timezone

__all__ = ['ReservationDateValidator']

# ---------------------------------- #
# Time when the room can be reserved #
# As default from 9 a.m to 9 p.m     #
# ---------------------------------- #

TIME_START_RESERVE = t(9, 00)
TIME_END_RESERVE = t(21, 00)


# ---------------------------------------------------------- #
# Now ReservationDateValidator also checks for multiplicity  #
# of 30 minutes. That is not best practice and in another    #
# version it will be replaced by Field Validators.           #
# ---------------------------------------------------------- #


class ReservationDateValidator(object):
    """
    Class provides a basic interface for validate date and time.

        `self._date`: date, YY-MM-DD
        `self._start`: time, HH:MM:SS:
        `self._end`: time, HH:MM:SS:

        `self.exc_class`: exception class for raises
        `self.timezone_now`: default timezone (optional)
        `self.start_date`: compared date and time
        `self.timezone_now`: compared date and time
    """

    def __init__(self, date, start, end, exc_class, **kwargs):
        self._date = date
        self._start = start
        self._end = end
        self.exc_class = exc_class

        self.timezone_now = kwargs.get("timezone")
        self.start_date = None
        self.end_date = None

    @staticmethod
    def convert_time_to_date(date, time):
        """Method convert input date and time to datetime obj"""
        return datetime.combine(date, time)

    def validate(self):
        """Start validate"""
        self.configure_timezone()
        self.configure_date()

        self.check_time()
        self.check_interval()
        self.check_multiple()

    def configure_date(self):
        """Setting up `start_date` and `end_date` to CTOR"""
        self.start_date = self.convert_time_to_date(self._date, self._start)
        self.end_date = self.convert_time_to_date(self._date, self._end)

    def configure_timezone(self):
        """Setting up current timezone if it is not"""
        if self.timezone_now is None:
            self.timezone_now = timezone.now()  # TODO fix if TIMEZONE

    def check_time(self):
        """Raise exception if now less than start date or end date"""
        if not self.timezone_now < self.start_date < self.end_date:
            msg = "End time must be greater than start time and start time must be greater than {}".format(
                self.timezone_now.strftime("%d-%m-%Y %H:%M")
            )
            raise self.exc_class(msg)

    def check_interval(self):
        """Raise exception if start time or end time not in interval"""
        for _t in (self._start, self._end):
            if not TIME_START_RESERVE < _t < TIME_END_RESERVE:
                msg = "You can reserve a room between 9 a.m. and 9 p.m"
                raise self.exc_class(msg)

    def check_multiple(self):
        """Raise exception if time minutes is not a multiple of 30 minutes"""
        minutes = (00, 30)  # 00 == 0
        for _t in (self._start, self._end):
            if _t.minute not in minutes:
                msg = 'You can only reserve a time that is a multiple of 30 minutes'
                raise self.exc_class(msg)
