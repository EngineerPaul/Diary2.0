from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from root.settings import PROJECT_HOSTS


class LoginRequiredMixin:
    """Миксин для проверки аутентификации пользователя"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.get('is_auth', False):
            return HttpResponseRedirect('/login')
        return super().dispatch(request, *args, **kwargs)


class RegistrationPage(TemplateView):
    template_name = 'frontend/registration.html'


class LoginPage(TemplateView):
    template_name = 'frontend/login.html'


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/index.html'


class HelpPage(TemplateView):  # удалить!
    template_name = 'frontend/help.html'


class OtherPage(TemplateView):  # удалить!
    template_name = 'frontend/other.html'


class SettingsPage(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/settings.html'


class SearchPage(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/search.html'


class NotePage(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/note.html'


class NoticePage(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/notice.html'
