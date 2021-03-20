from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, m2m_changed

from game.models import Perk, ItemAddOn, PowerAddOn, Item, Offering

@receiver(m2m_changed, sender=Perk.rarities.through)
def limit_perk_rarities(sender, instance, *args, **kwargs):
    if instance.rarities.count() > 3:
        raise ValidationError("You can't assign more than 3 rarities.")


@receiver(m2m_changed, sender=Item.rarities.through)
def limit_item_rarities(sender, instance, *args, **kwargs):
    if instance.rarities.count() > 1:
        raise ValidationError("You can't assign more than 1 rarity")


@receiver(m2m_changed, sender=ItemAddOn.rarities.through)
def limit_item_addon_rarities(sender, instance, *args, **kwargs):
    if instance.rarities.count() > 1:
        raise ValidationError("You can't assign more than 1 rarity.")


@receiver(m2m_changed, sender=PowerAddOn.rarities.through)
def limit_power_addon_rarities(sender, instance, *args, **kwargs):
    if instance.rarities.count() > 1:
        raise ValidationError("You can't assign more than 1 rarity.")


@receiver(m2m_changed, sender=Offering.rarities.through)
def limit_offering_rarities(sender, instance, *args, **kwargs):
    if instance.rarities.count() > 1:
        raise ValidationError("You can't assign more than 1 rarity")

        