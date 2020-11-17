import os
import re
import sys
import time
import zipfile
import tempfile
from pathlib import Path

# Needed to access Django ORM outside of manage.py
sys.path.append(
    "C:/Users/UserOne/Documents/Projects/dead-by-daylight-game-creator/server")
os.environ["DJANGO_SETTINGS_MODULE"] = "server.settings"
import django
django.setup()
from game.models import Character, Perk, Offering, Item, AddOn

# 1. Get all the icon packs
# 2. Let the user choose which icon pack to use
# 3. Once one is chosen, program will unzip the chosen pack
# 4. After unzipping, program will refactor the directories
# 5. After refactoring, program will create the new perk icons
# 6. After recreation, program will update image files in the DB

BASE_DIR = Path(__file__).resolve().parent.parent
ICONPACK_PATH = os.path.join(BASE_DIR, "assets\\_icon_packs")
OUTPUT_PATH = os.path.join(BASE_DIR, "assets\\templates")
ICONPACKS = os.listdir(ICONPACK_PATH)
TARGET_SUBDIRS = ["Favors", "ItemAddons", "Items", "Perks", "Powers"]
NORMALIZED_LEGACY_HEX_FILENAMES = [
    "Devour Hope", 
    "Ruin",
    "The Third Seal",
    "Thrill Of The Hunt", 
    "Haunted Ground",
    "Huntress Lullaby",
    "No One Escapes Death",
]

# Adds spaces between capital letters
def normalize(camelCase):
    return re.sub(r"(?<=\w)([A-Z])", r" \1", camelCase)

def is_sublist(list1, list2):
    res1 = [elem for elem in list1 if elem in list2]
    res2 = [elem for elem in list2 if elem in list1]
    return res1 == res2 and len(res1) > 0

def get_absolute_image_paths(directory):
    for path, _, file_list in os.walk(directory):
        for file in file_list:
            if "png" in file.lower():
                yield os.path.abspath(os.path.join(path, file))

print("===== Choose a Pack =====")
for idx, pack in enumerate(ICONPACKS):
    print(f"{idx}: {pack}")

opt = input("> ")
opt = int(opt)
if opt in range(0, len(ICONPACKS)):
    t1 = time.time()

    pack = ICONPACKS[opt]
    PATH  = os.path.join(ICONPACK_PATH, pack)

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(PATH, "r") as zf:
            zf.extractall(tmpdir)
            
            # Finding the parent directory to Perks, Items, etc.
            target_dir = None
            for path, subdir_list, file_list in os.walk(tmpdir):

                if is_sublist(TARGET_SUBDIRS, subdir_list):
                    target_dir = path
                    break

            dir_paths = [os.path.join(target_dir, path) 
            for path in os.listdir(target_dir) 
            if os.path.isdir(os.path.join(target_dir, path))
            ]

            icon_paths = set()
            for dpath in dir_paths:
                tokens = dpath.split("\\")
                folder = tokens.pop()
                if folder in ["StatusEffects", "Actions"]:
                    continue
                
                icon_paths = icon_paths.union(set(
                    get_absolute_image_paths(dpath)
                ))

            print(f"IconPaths: {len(icon_paths)}")
                
            for icon_path in icon_paths:
                filename = icon_path.split("\\").pop()
                tokens = filename.split("_")
                type = tokens[0][4:]
                
                # Name is camel case initially
                # Ex: selfCare, hexRetribution, wereGonnaLiveForever
                name = tokens[1].split(".")[0]

                # Capitlize first letter only, then add spaces
                # Ex: Self Care, Hex Retribution, Were Gonna Live Forever
                name = normalize(name[0].capitalize() + name[1:])
                

                type = type.lower()
                if type == "items":
                    destination = os.path.join(
                        os.path.join(OUTPUT_PATH, "items"),
                        filename)
                    os.replace(icon_path, destination)

                elif type == "powers":
                    destination = os.path.join(
                        os.path.join(OUTPUT_PATH, "powers"),
                        filename)
                    os.replace(icon_path, destination)
                                    
                elif type == "addon":
                    # Match addon, power or item?
                    destination = os.path.join(OUTPUT_PATH, "addons")
                    # os.rename(icon_path, destination)
                    
                elif type == "perks":
                    destination = os.path.join(OUTPUT_PATH, "perks")

                    # Special Cases
                    if name == "Self Care":
                        name = "Self-Care"

                    if name == "Were Gonna Live Forever":
                        name = "We're Gonna Live Forever"

                    if "Hex" in name:
                        # start at index 4 to account for space (i.e. "Hex ")
                        hex = normalize(name[4:])
                        name = f"Hex: {hex}"

                    if name in NORMALIZED_LEGACY_HEX_FILENAMES:
                        name = f"Hex: {name}"
                    
                    # Will return up to 3 Tiers for a Perk
                    perks = Perk.objects.filter(name=name)
                    if len(perks) > 0:
                        perk = perks[0]
                        perk_type = perk.type.lower()
                        print(perk_type)
                        os.replace(
                            icon_path,
                            os.path.join(
                                os.path.join(destination, perk_type), 
                                filename))

                elif type == "favors":
                    # Match offering, killer, survivor or ALL?
                    destination = os.path.join(OUTPUT_PATH, "offerings")
                    
                else:
                    print("Invalid type")
                    break

    t2 = time.time()
    time_elapsed = t2 - t1
    print(f"Unpacking completed. Time Elapsed: {time_elapsed} s")
else:
    print("Please enter a valid option.")

