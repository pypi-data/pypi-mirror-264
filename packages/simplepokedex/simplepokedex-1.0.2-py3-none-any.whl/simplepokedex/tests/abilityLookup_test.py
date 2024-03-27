import sys

sys.path.insert(1, "./simple-pokedex")

import lookup


# catching error when wrong ability is sent
def test_lookup_1():
    response = lookup.abilityLookup("minecraft")
    assert response == {"success": False, "message": 404, "data": None}


# catching error when no ability is sent
def test_lookup_2():
    response = lookup.abilityLookup("")
    assert response == {"success": False, "message": 400, "data": None}


# correct response for moxie
def test_lookup_3():
    response = lookup.abilityLookup("moxie")
    assert response == {
        "success": True,
        "message": "success",
        "data": "This Pokémon's Attack rises one stage upon knocking out another Pokémon, even a friendly Pokémon.\n\nThis ability does not take effect when the Pokémon indirectly causes another Pokémon to faint, e.g. through poison or spikes.\n\nIf this Pokémon knocks out a Pokémon with mummy, the former's ability will change without taking effect.",
    }


# correct response for intimidate
def test_lookup_4():
    response = lookup.abilityLookup("intimidate")
    assert response == {
        "success": True,
        "message": "success",
        "data": "When this Pokémon enters battle, the opponent's Attack is lowered by one stage.  In a double battle, both opponents are affected.\n\nThis ability also takes effect when acquired during a battle, but will not take effect again if lost and reobtained without leaving battle.\n\nThis ability has no effect on an opponent that has a substitute.\n\nOverworld: If the first Pokémon in the party has this ability, any random encounter with a Pokémon five or more levels lower than it has a 50% chance of being skipped.",
    }
