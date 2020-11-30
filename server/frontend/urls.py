from django.urls import include, path, re_path

from frontend import views

urlpatterns = [
    path("", views.index),
    path("join/", views.index),
    path("create/", views.index),
    path("session/", views.index),
]