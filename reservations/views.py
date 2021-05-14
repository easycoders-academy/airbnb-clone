import datetime
from django.http import Http404
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
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation:
            raise Http404()
        if (
            self.request.user != reservation.guest
            and self.request.user != reservation.room.host
        ):
            raise Http404()
        return render(
            self.request, "reservations/detail.html", {"reservation": reservation}
        )


def edit_reservation(request, pk, action):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation:
        raise Http404()
    if request.user != reservation.guest and request.user != reservation.room.host:
        raise Http404()
    if action == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif action == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Бронирование обновлено")
    return redirect(reverse("reservations:detail", kwargs={"pk": pk}))
