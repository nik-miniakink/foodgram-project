from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, base_user
from django import forms
User = get_user_model()


class CreationForm(UserCreationForm):
    email = forms.EmailField(label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email')