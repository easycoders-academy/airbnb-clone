from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):
    """ Описание модели отзывов """

    review = models.TextField()
    cleanliness = models.IntegerField()
    communication = models.IntegerField()
    checkin = models.IntegerField()
    accuracy = models.IntegerField()
    location = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.review}"

    def rating_average(self):
        avg = (
            self.cleanliness
            + self.communication
            + self.checkin
            + self.accuracy
            + self.location
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."
