from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_countries import countries
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):
    """ Определение представления HomeView """

    model = models.Room
    paginate_by = 12
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"


class RoomDetail(DetailView):
    """ Опредение представления RoomDetail """

    model = models.Room


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                bathrooms = form.cleaned_data.get("bathrooms")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Везде":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if bathrooms is not None:
                    filter_args["bathrooms__gte"] = bathrooms

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},
                )
        else:
            form = forms.SearchForm()

        return render(
            request,
            "rooms/search.html",
            {"form": form},
        )


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "beds",
        "bedrooms",
        "bathrooms",
        "guests",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Невозможно удалить фотографию")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Фотография удалена")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
