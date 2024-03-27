import sys

sys.path.insert(1, "./simple-pokedex")

import lookup


# correct output
def test_lookup_1():
    response = lookup.pokemonLookup("ditto")
    assert response == {
        "success": True,
        "message": "success",
        "data": {
            "name": "ditto",
            "id": 132,
            "types": ["NORMAL"],
            "stats": [
                {
                    "base_stat": 48,
                    "effort": 1,
                    "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
                },
                {
                    "base_stat": 48,
                    "effort": 0,
                    "stat": {
                        "name": "attack",
                        "url": "https://pokeapi.co/api/v2/stat/2/",
                    },
                },
                {
                    "base_stat": 48,
                    "effort": 0,
                    "stat": {
                        "name": "defense",
                        "url": "https://pokeapi.co/api/v2/stat/3/",
                    },
                },
                {
                    "base_stat": 48,
                    "effort": 0,
                    "stat": {
                        "name": "special-attack",
                        "url": "https://pokeapi.co/api/v2/stat/4/",
                    },
                },
                {
                    "base_stat": 48,
                    "effort": 0,
                    "stat": {
                        "name": "special-defense",
                        "url": "https://pokeapi.co/api/v2/stat/5/",
                    },
                },
                {
                    "base_stat": 48,
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
                        "name": "limber",
                        "url": "https://pokeapi.co/api/v2/ability/7/",
                    },
                    "is_hidden": False,
                    "slot": 1,
                },
                {
                    "ability": {
                        "name": "imposter",
                        "url": "https://pokeapi.co/api/v2/ability/150/",
                    },
                    "is_hidden": True,
                    "slot": 3,
                },
            ],
        },
    }


# failed test where the search is not a real pokemon
def test_lookup_2():
    response = lookup.pokemonLookup("minecraft")
    print(response)
    assert response == {"success": False, "message": 404, "data": None}


# correct response for pikachu
def test_lookup_3():
    response = lookup.pokemonLookup("pikachu")
    assert response == {
        "success": True,
        "message": "success",
        "data": {
            "name": "pikachu",
            "id": 25,
            "types": ["ELECTRIC"],
            "stats": [
                {
                    "base_stat": 35,
                    "effort": 0,
                    "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
                },
                {
                    "base_stat": 55,
                    "effort": 0,
                    "stat": {
                        "name": "attack",
                        "url": "https://pokeapi.co/api/v2/stat/2/",
                    },
                },
                {
                    "base_stat": 40,
                    "effort": 0,
                    "stat": {
                        "name": "defense",
                        "url": "https://pokeapi.co/api/v2/stat/3/",
                    },
                },
                {
                    "base_stat": 50,
                    "effort": 0,
                    "stat": {
                        "name": "special-attack",
                        "url": "https://pokeapi.co/api/v2/stat/4/",
                    },
                },
                {
                    "base_stat": 50,
                    "effort": 0,
                    "stat": {
                        "name": "special-defense",
                        "url": "https://pokeapi.co/api/v2/stat/5/",
                    },
                },
                {
                    "base_stat": 90,
                    "effort": 2,
                    "stat": {
                        "name": "speed",
                        "url": "https://pokeapi.co/api/v2/stat/6/",
                    },
                },
            ],
            "abilities": [
                {
                    "ability": {
                        "name": "static",
                        "url": "https://pokeapi.co/api/v2/ability/9/",
                    },
                    "is_hidden": False,
                    "slot": 1,
                },
                {
                    "ability": {
                        "name": "lightning-rod",
                        "url": "https://pokeapi.co/api/v2/ability/31/",
                    },
                    "is_hidden": True,
                    "slot": 3,
                },
            ],
        },
    }
