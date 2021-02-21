# This module will generate the Icons using the images in templates/
# and attach them to their respective Models

# Every entry in the DB that has an image file will be called and reupdated

import os
import sys
import time
import tempfile
from io import BytesIO
from pathlib import Path

from django.core.files import File

from PIL import Image

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
ASSETS_PATH = os.path.join(BASE_DIR, "assets")
TEMPLATES_PATH = os.path.join(BASE_DIR, "assets\\templates")

def generate_model_image(model, border):
    BORDERS_PATH = os.path.join(TEMPLATES_PATH, f"borders\\{border}")

    time1 = time.time()
    for element in model.objects.all():
        with Image.open(element.template) as template:
            rarity = str(element.rarity).replace(" ", "-").lower()
            
            borders = [os.path.join(BORDERS_PATH, file)
                for file in os.listdir(BORDERS_PATH)
                if file.split(".")[0] == rarity
            ]

            if len(borders) == 1:
                with Image.open(borders[0]) as background:
                    name = str(element.name).replace("'", "").replace(" ", "_")
                    background.paste(template, (0,0), mask=template)

                    buff = BytesIO()
                    background.save(buff, "PNG")

                    element.image.save(f"{name}.png", File(buff), save=False)
                    element.save()

    time_elapsed = time.time() - time1
    print(f"Generated {model.__name__} images in {time_elapsed} secs")

def generate_power_images():
    BORDER_PATH = os.path.join(TEMPLATES_PATH, f"borders\\square\\common.png")
    time1 = time.time()
    for element in Power.objects.all():
        with Image.open(BORDER_PATH) as background:                
            with Image.open(element.primary_template) as template:
                name = str(element.name).replace("'", "").replace(" ", "_")
                name = name + "-primary"
                background.paste(template, (0,0), mask=template)

                buff = BytesIO()
                background.save(buff, "PNG")

                element.primary_image.save(
                    f"{name}.png", 
                    File(buff), 
                    save=False
                )

            if element.secondary_template:
                with Image.open(element.secondary_template) as template:
                    name = str(element.name).replace("'", "").replace(" ", "_")
                    name = name + "-secondary"
                    background.paste(template, (0,0), mask=template)

                    buff = BytesIO()
                    background.save(buff, "PNG")

                    element.secondary_image.save(
                        f"{name}.png", 
                        File(buff), 
                        save=False
                    )

            if element.tertiary_template:
                with Image.open(element.tertiary_template) as template:
                    name = str(element.name).replace("'", "").replace(" ", "_")
                    name = name + "-tertiary"
                    background.paste(template, (0,0), mask=template)

                    buff = BytesIO()
                    background.save(buff, "PNG")

                    element.tertiary_image.save(
                        f"{name}.png", 
                        File(buff), 
                        save=False
                    )    
        element.save()
        

    time_elapsed = time.time() - time1
    print(f"Generated Power images in {time_elapsed} secs")

generate_model_image(Item, "square")
generate_model_image(Perk, "dsquare")
generate_model_image(Offering, "hex")
generate_power_images()

# ITEM_BORDERS_PATH = os.path.join(TEMPLATES_PATH, "borders\\square")
# for item in Item.objects.all():        
#     with Image.open(item.template) as template:
#         rarity = str(item.rarity).replace(" ", "-").lower()
#         borders = [os.path.join(ITEM_BORDERS_PATH, file) 
#             for file in os.listdir(
#                 os.path.join(TEMPLATES_PATH, "borders\\square")
#             ) 
#             if file.split(".")[0] == rarity 
#         ]
        
#         if len(borders) == 1:
#             with Image.open(borders[0]) as background:
#                 name = str(item.name).replace("'", "").replace(" ", "_")
#                 # file_path = os.path.join(tmpdir, f"{name}.png")
#                 # print(file_path)
#                 background.paste(template, (0,0), mask=template)
                
#                 buff = BytesIO()
#                 background.save(buff, "PNG")

#                 item.image.save(f"{name}.png", File(buff), save=False)
#                 item.save()

# PERK_BORDERS_PATH = os.path.join(TEMPLATES_PATH, "borders\\dsquare")
# for perk in Perk.objects.all():
#     with Image.open(perk.template) as template:
#         rarity = str(item.rarity).replace(" ", "-").lower()            
#         borders = [os.path.join(PERK_BORDERS_PATH, file)
#             for file in os.listdir(
#                 os.path.join(TEMPLATES_PATH, "borders\\dsquare")
#             )
#             if file.split(".")[0] == rarity
#         ]

    # Start putting together perk icons

