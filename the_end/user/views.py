from django.views.generic import CreateView

from .forms import CreationForm

class SignUp(CreateView):
    """
    Отображает форму авторизации/регистрации
    """
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html"
