from django.contrib import admin

from game.models import (
    Character,
    Effect, EffectType,
    Item, ItemType, AddOn,
    Offering,
    Perk,
    Rarity
)

admin.site.register(Character)
admin.site.register(Effect)
admin.site.register(EffectType)
admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(AddOn)
admin.site.register(Offering)
admin.site.register(Perk)
admin.site.register(Rarity)