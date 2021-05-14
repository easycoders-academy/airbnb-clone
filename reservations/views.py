import datetime
from django.views.generic import View
from django.contrib import messages
from rooms import models as room_models
from . import models
from django.shortcuts import render, redirect, reverse


class CreateException(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateException()
    except (room_models.Room.DoesNotExist, CreateException):
        messages.error(request, "Невозможно создать бронирование")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, pk):
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation:
            redirect(reverse("core:home"))
