from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Определение админки для объектов """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Определение админки для фотографий """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Preview"


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Определение админки для жилья """

    inlines = [
        PhotoInline,
    ]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "description",
                    "room_type",
                    "country",
                    "city",
                    "address",
                    "price",
                )
            },
        ),
        ("Время заезда/выезда", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Спальные места", {"fields": ("beds", "bedrooms", "bathrooms", "guests")}),
        (
            "Удобства",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        ("Дополнительная информация", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "beds",
        "bedrooms",
        "bathrooms",
        "guests",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "host__superhost",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    raw_id_fields = ("host",)

    search_fields = ("=city", "^host__username")

    filter_horizontal = ("amenities", "facilities", "house_rules")

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"
