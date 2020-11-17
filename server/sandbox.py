import os

from PIL import Image

ROOT = "assets/templates"
size = (100, 100)



# Perks can only be "Uncommon", "Rare", "Very Rare", or "Teachable" rarity
with Image.open(os.path.join(ROOT, "perks/iconPerks_adrenaline.png")) as perk:
    template = os.path.join(ROOT, "borders/dsquare")

    for filename in os.listdir(template):
        rarity = filename.split(".")[0]
        if rarity.lower() == "uncommon":
            tier = 1
        elif rarity.lower() == "rare":
            tier = 2
        elif rarity.lower() == "very-rare":
            tier = 3
        elif rarity.lower() == "teachable":
            tier = rarity
        else:
            continue

        with Image.open(os.path.join(template, filename)) as bg:
            bg.paste(perk, (0,0), mask=perk)
            bg = bg.resize(size)
            bg.save(f"assets/perks/survivor/adrenaline-{tier}.png", "PNG")