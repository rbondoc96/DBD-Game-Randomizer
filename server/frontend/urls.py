from django.urls import include, path, re_path

from frontend import views

urlpatterns = [
    path("", views.index),
    path("about/", views.index),
    re_path(r"^sessions/$", views.index),
    re_path(r"^sessions/(?P<sessionId>[A-Z0-9a-z]{6})/$", views.index),
    path("settings/", views.index),
    path("create/", views.index),
]