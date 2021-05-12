from django.db import models
from django.utils import timezone
from core import models as core_models


class BoookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"


class Reservation(core_models.TimeStampedModel):
    """ Описание модели бронирований """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Ожидание подтверждения"),
        (STATUS_CONFIRMED, "Подтверждено"),
        (STATUS_CANCELED, "Отменено"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    def save(self, *args, **kwargs):
        if True:
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BoookedDay.objects.filter(
                day__range=(start, end)
            ).exists()

            if existing_booked_day == False:
                

        return super().save(*args, **kwargs)

    in_progress.boolean = True
    is_finished.boolean = True
