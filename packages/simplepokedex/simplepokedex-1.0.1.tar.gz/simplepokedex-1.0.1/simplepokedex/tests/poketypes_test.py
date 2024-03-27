import sys

sys.path.insert(1, "./simple-pokedex")
import poketypes


def test_poketypes():
    response = poketypes.poketypes("poison")
    assert response == {
        "success": True,
        "message": "success",
        "data": {
            "double_damage_from": [
                {"name": "ground", "url": "https://pokeapi.co/api/v2/type/5/"},
                {"name": "psychic", "url": "https://pokeapi.co/api/v2/type/14/"},
            ],
            "double_damage_to": [
                {"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"},
                {"name": "fairy", "url": "https://pokeapi.co/api/v2/type/18/"},
            ],
            "half_damage_from": [
                {"name": "fighting", "url": "https://pokeapi.co/api/v2/type/2/"},
                {"name": "poison", "url": "https://pokeapi.co/api/v2/type/4/"},
                {"name": "bug", "url": "https://pokeapi.co/api/v2/type/7/"},
                {"name": "grass", "url": "https://pokeapi.co/api/v2/type/12/"},
                {"name": "fairy", "url": "https://pokeapi.co/api/v2/type/18/"},
            ],
            "half_damage_to": [
                {"name": "poison", "url": "https://pokeapi.co/api/v2/type/4/"},
                {"name": "ground", "url": "https://pokeapi.co/api/v2/type/5/"},
                {"name": "rock", "url": "https://pokeapi.co/api/v2/type/6/"},
                {"name": "ghost", "url": "https://pokeapi.co/api/v2/type/8/"},
            ],
            "no_damage_from": [],
            "no_damage_to": [
                {"name": "steel", "url": "https://pokeapi.co/api/v2/type/9/"}
            ],
        },
    }


def test_poketypes2():
    response = poketypes.poketypes("fairy")
    assert response == {
        "success": True,
        "message": "success",
        "data": {
            "double_damage_from": [
                {"name": "poison", "url": "https://pokeapi.co/api/v2/type/4/"},
                {"name": "steel", "url": "https://pokeapi.co/api/v2/type/9/"},
            ],
            "double_damage_to": [
                {"name": "fighting", "url": "https://pokeapi.co/api/v2/type/2/"},
                {"name": "dragon", "url": "https://pokeapi.co/api/v2/type/16/"},
                {"name": "dark", "url": "https://pokeapi.co/api/v2/type/17/"},
            ],
            "half_damage_from": [
                {"name": "fighting", "url": "https://pokeapi.co/api/v2/type/2/"},
                {"name": "bug", "url": "https://pokeapi.co/api/v2/type/7/"},
                {"name": "dark", "url": "https://pokeapi.co/api/v2/type/17/"},
            ],
            "half_damage_to": [
                {"name": "poison", "url": "https://pokeapi.co/api/v2/type/4/"},
                {"name": "steel", "url": "https://pokeapi.co/api/v2/type/9/"},
                {"name": "fire", "url": "https://pokeapi.co/api/v2/type/10/"},
            ],
            "no_damage_from": [
                {"name": "dragon", "url": "https://pokeapi.co/api/v2/type/16/"}
            ],
            "no_damage_to": [],
        },
    }


def test_poketypes3():
    response = poketypes.poketypes("palworld")
    assert response == {"success": False, "message": 404, "data": None}
