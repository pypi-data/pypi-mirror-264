import sys

sys.path.insert(1, "./simple-pokedex")
import generatePokemon


def test_generate_1():
    response = generatePokemon.generate_pokemon(4, 123)
    assert response == {
        "success": True,
        "message": "success",
        "data": {
            "name": "shinx",
            "id": 403,
            "types": ["ELECTRIC"],
            "stats": [
                {
                    "base_stat": 45,
                    "effort": 0,
                    "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
                },
                {
                    "base_stat": 65,
                    "effort": 1,
                    "stat": {
                        "name": "attack",
                        "url": "https://pokeapi.co/api/v2/stat/2/",
                    },
                },
                {
                    "base_stat": 34,
                    "effort": 0,
                    "stat": {
                        "name": "defense",
                        "url": "https://pokeapi.co/api/v2/stat/3/",
                    },
                },
                {
                    "base_stat": 40,
                    "effort": 0,
                    "stat": {
                        "name": "special-attack",
                        "url": "https://pokeapi.co/api/v2/stat/4/",
                    },
                },
                {
                    "base_stat": 34,
                    "effort": 0,
                    "stat": {
                        "name": "special-defense",
                        "url": "https://pokeapi.co/api/v2/stat/5/",
                    },
                },
                {
                    "base_stat": 45,
                    "effort": 0,
                    "stat": {
                        "name": "speed",
                        "url": "https://pokeapi.co/api/v2/stat/6/",
                    },
                },
            ],
            "abilities": [
                {
                    "ability": {
                        "name": "rivalry",
                        "url": "https://pokeapi.co/api/v2/ability/79/",
                    },
                    "is_hidden": False,
                    "slot": 1,
                },
                {
                    "ability": {
                        "name": "intimidate",
                        "url": "https://pokeapi.co/api/v2/ability/22/",
                    },
                    "is_hidden": False,
                    "slot": 2,
                },
                {
                    "ability": {
                        "name": "guts",
                        "url": "https://pokeapi.co/api/v2/ability/62/",
                    },
                    "is_hidden": True,
                    "slot": 3,
                },
            ],
        },
    }


def test_generate_2():
    response = generatePokemon.generate_pokemon(5, 111)
    assert response == {
        "success": True,
        "message": "success",
        "data": {
            "name": "archen",
            "id": 566,
            "types": ["ROCK", "FLYING"],
            "stats": [
                {
                    "base_stat": 55,
                    "effort": 0,
                    "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
                },
                {
                    "base_stat": 112,
                    "effort": 1,
                    "stat": {
                        "name": "attack",
                        "url": "https://pokeapi.co/api/v2/stat/2/",
                    },
                },
                {
                    "base_stat": 45,
                    "effort": 0,
                    "stat": {
                        "name": "defense",
                        "url": "https://pokeapi.co/api/v2/stat/3/",
                    },
                },
                {
                    "base_stat": 74,
                    "effort": 0,
                    "stat": {
                        "name": "special-attack",
                        "url": "https://pokeapi.co/api/v2/stat/4/",
                    },
                },
                {
                    "base_stat": 45,
                    "effort": 0,
                    "stat": {
                        "name": "special-defense",
                        "url": "https://pokeapi.co/api/v2/stat/5/",
                    },
                },
                {
                    "base_stat": 70,
                    "effort": 0,
                    "stat": {
                        "name": "speed",
                        "url": "https://pokeapi.co/api/v2/stat/6/",
                    },
                },
            ],
            "abilities": [
                {
                    "ability": {
                        "name": "defeatist",
                        "url": "https://pokeapi.co/api/v2/ability/129/",
                    },
                    "is_hidden": False,
                    "slot": 1,
                }
            ],
        },
    }


def test_generate_3():
    response = generatePokemon.generate_pokemon(10)
    assert response == {"success": False, "message": "404", "data": None}


def test_generate_4():
    response = generatePokemon.generate_pokemon(0, 555)
    assert response == {
        "success": True,
        "message": "success",
        "data": {
            "name": "infernape",
            "id": 392,
            "types": ["FIRE", "FIGHTING"],
            "stats": [
                {
                    "base_stat": 76,
                    "effort": 0,
                    "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
                },
                {
                    "base_stat": 104,
                    "effort": 1,
                    "stat": {
                        "name": "attack",
                        "url": "https://pokeapi.co/api/v2/stat/2/",
                    },
                },
                {
                    "base_stat": 71,
                    "effort": 0,
                    "stat": {
                        "name": "defense",
                        "url": "https://pokeapi.co/api/v2/stat/3/",
                    },
                },
                {
                    "base_stat": 104,
                    "effort": 1,
                    "stat": {
                        "name": "special-attack",
                        "url": "https://pokeapi.co/api/v2/stat/4/",
                    },
                },
                {
                    "base_stat": 71,
                    "effort": 0,
                    "stat": {
                        "name": "special-defense",
                        "url": "https://pokeapi.co/api/v2/stat/5/",
                    },
                },
                {
                    "base_stat": 108,
                    "effort": 1,
                    "stat": {
                        "name": "speed",
                        "url": "https://pokeapi.co/api/v2/stat/6/",
                    },
                },
            ],
            "abilities": [
                {
                    "ability": {
                        "name": "blaze",
                        "url": "https://pokeapi.co/api/v2/ability/66/",
                    },
                    "is_hidden": False,
                    "slot": 1,
                },
                {
                    "ability": {
                        "name": "iron-fist",
                        "url": "https://pokeapi.co/api/v2/ability/89/",
                    },
                    "is_hidden": True,
                    "slot": 3,
                },
            ],
        },
    }
