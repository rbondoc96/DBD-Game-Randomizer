# This module will generate the Icons using the images in templates/
# and attach them to their respective Models

# Every entry in the DB that has an image file will be called and reupdated

import os
import sys
import time
from pathlib import Path

# Needed to access Django ORM outside of manage.py
sys.path.append(
    "C:/Users/UserOne/Documents/Projects/dead-by-daylight-game-creator/server")
os.environ["DJANGO_SETTINGS_MODULE"] = "server.settings"
import django
django.setup()
from game.models import (
    Character, Perk, Offering, 
    Item, ItemAddOn, 
    Power, PowerAddOn
)

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_PATH = os.path.join(BASE_DIR, "assets\\templates")

def generate_image(name, type):
    pass

# Convert Items
# item.image -- template overlay
# templates/borders -- icon pg
ITEMS_PATH = os.path.join(TEMPLATES_PATH, "items")
for item in Item.objects.all():
    pass

