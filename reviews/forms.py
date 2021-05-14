from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = (
            "review",
            "cleanliness",
            "communication",
            "checkin",
            "accuracy",
            "location",
            "value",
        )