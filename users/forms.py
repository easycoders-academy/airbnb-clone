from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "rounded-b-none", "placeholder": "Email"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "mb-4 rounded-t-none", "placeholder": "Пароль"}
        )
    )

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
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "rounded-t-none rounded-b-none", "placeholder": "Пароль"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "rounded-t-none mb-4", "placeholder": "Повторите пароль"}
        )
    )

    class Meta:
        model = models.User
        fields = ("username", "first_name", "last_name")
        widgets = {
            "username": forms.EmailInput(
                attrs={"class": "rounded-t-none rounded-b-none", "placeholder": "Email"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "rounded-b-none", "placeholder": "Введите имя"}
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "rounded-b-none rounded-t-none",
                    "placeholder": "Введите фамилию",
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["username"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
