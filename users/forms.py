from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Пароль неверный"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("Пользователь не существует"))


class SignUpForm(UserCreationForm):
    username = forms.EmailField(label="Email")

    class Meta:
        model = models.User
        fields = ("username", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
