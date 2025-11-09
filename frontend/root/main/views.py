from django.views.generic import TemplateView


class RegistrationPage(TemplateView):
    template_name = 'frontend/registration.html'


class LoginPage(TemplateView):
    template_name = 'frontend/login.html'


class HomePage(TemplateView):
    template_name = 'frontend/index.html'


class HelpPage(TemplateView):  # удалить!
    template_name = 'frontend/help.html'


class OtherPage(TemplateView):  # удалить!
    template_name = 'frontend/other.html'


class SettingsPage(TemplateView):
    template_name = 'frontend/settings.html'


class SearchPage(TemplateView):
    template_name = 'frontend/search.html'


class NotePage(TemplateView):
    template_name = 'frontend/note.html'


class NoticePage(TemplateView):
    template_name = 'frontend/notice.html'
