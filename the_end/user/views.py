
from django.urls import reverse_lazy
from django.views.generic import CreateView
# from django.contrib.auth.urls import
from .forms import CreationForm

class SignUp(CreateView):
    """
    Отображает форму авторизации/регистрации
    """
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html"
