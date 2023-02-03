from django.urls import path, re_path
from . import views

urlpatterns = [
    path('uploads/form/', views.model_form_upload, name="converter"),
    path('uploads/', views.page),
    re_path(r'uploads/(?P<task_id>[0-9A-Za-z]{32}/)', views.page, name="converter_page"),
    re_path(r'uploads/status/(?P<task_id>[0-9A-Za-z]{32})/', views.status, name="converter_status"),
]