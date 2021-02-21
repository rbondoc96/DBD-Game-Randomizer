from django.contrib import admin

from game.models import (
    Character,
    Condition, ConditionType,
    Effect, EffectType,
    Modifier, ModifierType, ModifierUnit,
    Item, ItemType, ItemAddOn,
    Power, PowerAddOn,
    Offering,
    Perk,
    Rarity,
    Realm,
    Player,
    Session,
    Event
)

admin.site.register(Character)
admin.site.register(Effect)
admin.site.register(Condition)
admin.site.register(ConditionType)
admin.site.register(Modifier)
admin.site.register(ModifierType)
admin.site.register(ModifierUnit)
admin.site.register(EffectType)
admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(ItemAddOn)
admin.site.register(Power)
admin.site.register(PowerAddOn)
admin.site.register(Offering)
admin.site.register(Perk)
admin.site.register(Rarity)
admin.site.register(Player)
admin.site.register(Session)
admin.site.register(Event)
admin.site.register(Realm)