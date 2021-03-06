"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sessions.models import Session

from django.conf import settings
from django.conf.urls.static import static

from game.models import Player
from game.utils.logs import Logger

TAG = "TopURLs"
logger = Logger(TAG)

def server_init():
    logger.debug("Initializing server")

    # Clear Players, therefore clearing all Sessions
    Player.objects.all().delete()
    logger.debug("All players deleted.")
        

urlpatterns = [
    path("", include("frontend.urls")),
    path("", include("game.urls")),
    path('admin/', admin.site.urls),
]

# Allows images uploaded by a user to be served during development
# DO NOT use for production
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT)

server_init() 