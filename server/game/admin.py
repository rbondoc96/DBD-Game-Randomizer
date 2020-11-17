from django.contrib import admin

from game.models import (
    Character,
    Effect, EffectType,
    Item, ItemType, ItemAddOn,
    Power, PowerAddOn,
    Offering,
    Perk,
    Rarity
)

admin.site.register(Character)
admin.site.register(Effect)
admin.site.register(EffectType)
admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(ItemAddOn)
admin.site.register(Power)
admin.site.register(PowerAddOn)
admin.site.register(Offering)
admin.site.register(Perk)
admin.site.register(Rarity)