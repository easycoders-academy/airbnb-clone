from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    communication = forms.IntegerField(max_value=5, min_value=1)
    checkin = forms.IntegerField(max_value=5, min_value=1)
    accuracy = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    value = forms.IntegerField(max_value=5, min_value=1)

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

    def save(self, *args, **kwargs):
        review = super().save(commit=False)
        return review