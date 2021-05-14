from . import forms
from rooms import models as rooms_models
from django.shortcuts import redirect, reverse
from django.contrib import messages


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = rooms_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Отзыв отправлен")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
