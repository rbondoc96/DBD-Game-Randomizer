from random import sample, randint

from game.models import(
    Player,
    Character,
    Offering,
    Perk,
    Item, Power,
    ItemAddOn, PowerAddOn,
)

def get_random_index(iterable):
    return sample(range(0, len(iterable)), 1)[0]

def generate_random_player(role, no_licensed_chars=False):
    role__proper = role.title()
    player = {
        "role": role__proper,
    }

    if no_licensed_chars:
        characters = Character.objects.filter(
            type=role__proper,
        ).exclude(is_licensed=True)
    else:
        characters = Character.objects.filter(type=role__proper)
    
    character = characters[get_random_index(characters)]
    player["character"] = character

    offering = None
    if randint(0,3):
        offerings = Offering.objects.all()
        offering = offerings[get_random_index(offerings)]
        player["offering"] = offering
    
    item = None
    power = None
    if role == "survivor":
        items = Item.objects.all()
        item = items[get_random_index(items)]
        player["item"] = item

    # Need to returns killer's respective power
    elif role == "killer":
        power = Power.objects.all()[0]
        player["power"] = power

    PLAYER = Player.objects.create(
        **player
    )

    perk_set = Perk.objects.filter(type=role__proper)
    for _ in range(0, 4):
        PLAYER.perks.add(
            perk_set[get_random_index(perk_set)]
        )
        
    PLAYER.save()
    return PLAYER