from django.urls import include, path, re_path

from frontend import views

urlpatterns = [
    path("", views.index, name="index"),
]