from django import forms
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


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=80, label="Имя")
    last_name = forms.CharField(max_length=80, label="Фамилия")
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Подтверждение пароля"
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("Пользователь уже существует")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Пароли не совпадают")
        else:
            return password

    def save(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
