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


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email"]

    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password1 = forms.CharField(
        widget=forms.PasswordInput, label="Подтверждение пароля"
    )

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Пароли не совпадают")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        username = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = username
        user.set_password(password)
        user.save()
