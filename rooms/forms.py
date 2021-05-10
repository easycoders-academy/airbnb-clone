from django import forms
from . import models
from django_countries.fields import CountryField


class SearchForm(forms.Form):
    city = forms.CharField(initial="Везде")
    country = CountryField(default="RU").formfield()
    room_type = forms.ModelChoiceField(
        required=False,
        queryset=models.RoomType.objects.all(),
        empty_label="Любой тип жилья",
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    bathrooms = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        models.Room.objects.get(pk=pk)
        photo = super().save(commit=False)