from django.urls import path

from .views import (
    HomePage, HelpPage, OtherPage, SettingsPage, SearchPage,
    NotePage, NoticePage,
    LoginPage, RegistrationPage,
)


urlpatterns = [
    path('', HomePage.as_view(), name='home_url'),
    path('help', HelpPage.as_view(), name='help_url'),
    path('other', OtherPage.as_view(), name='other_url'),
    path('settings', SettingsPage.as_view(), name='settings_url'),
    path('searching', SearchPage.as_view(), name='search_url'),
    path('notes/<int:pk>/', NotePage.as_view(), name='note_url'),
    path('notices/<int:pk>/', NoticePage.as_view(), name='note_url'),

    path('registration', RegistrationPage.as_view(), name='registration_url'),
    path('login', LoginPage.as_view(), name='login_url'),
]
