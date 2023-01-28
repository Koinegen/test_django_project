from django.urls import path, re_path
from . import views as core_views


urlpatterns = [
    path('signup/', core_views.signup, name='signup'),
    path('account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]*)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
        core_views.activate, name='activate')
    # re_path(r'activate/(?P<uidb64>.*)/(?P<token>.*)', core_views.activate, name='activate')
]
