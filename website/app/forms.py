from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm


class create_user_form(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "input", "placeholder": "Enter your email"}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "input", "placeholder": "Enter your first name"}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "input", "placeholder": "Enter your surname"}))

    class Meta:
        model = User
        fields = {"username", "first_name", "last_name",
                  "email", "password1", "password2"}

    def __init__(self, *args, **kwargs):
        super(create_user_form, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "input"
        self.fields["username"].widget.attrs[
            "placeholder"] = "Enter your username"
        self.fields["password1"].widget.attrs["class"] = "input"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter your password"
        self.fields["password1"].widget.attrs["id"] = "password1"
        self.fields["password2"].widget.attrs["class"] = "input"
        self.fields["password2"].widget.attrs["placeholder"] = "Enter your password again"
        self.fields["password2"].widget.attrs["id"] = "password2"


class update_user_details_form(create_user_form):
    class Meta:
        model = User
        fields = {"username", "first_name", "last_name",
                  "email", "password1"}

    def __init__(self, *args, **kwargs):
        super(update_user_details_form, self).__init__(*args, **kwargs)
        self.fields.pop('password2')


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': 'Enter your email',
        'type': 'email',
        'name': 'email'
    }))
