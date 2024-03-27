import requests
import random

def generate_pokemon(gen = 0, seed = 0):
    if seed != 0:
        random.seed(seed)
    if gen == 0:
        gen = random.randint(1, 9)
    r = requests.get(f"https://pokeapi.co/api/v2/generation/{gen}")
    # handle invalid input and API errors
    if r.status_code == 404:
        return {"success": False, "message": f"{r.status_code}", "data": None}
    if r.status_code != 200:
        return {"success": False, "data": f"{r.status_code}", "data": None}
    
    data = r.json()
    pokemon = random.choice(data["pokemon_species"])
    url = pokemon["url"].replace("-species", "")
    rawData = requests.get(url).json()
    pokemonData = {
        "name": rawData["name"],
        "id": rawData["id"],
        "types": [t["type"]["name"].upper() for t in rawData["types"]],
        "stats": rawData["stats"],
        "abilities": rawData["abilities"]
    }
    return {"success": True, "message": "success", "data": pokemonData}


def pokemonLookup(pokemon=""):
    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "message": "success",
            "data": {
                "name": data["name"],
                "id": data["id"],
                "types": [type["type"]["name"].upper() for type in data["types"]],
                "stats": data["stats"],
                "abilities": data["abilities"],
            },
        }
    else:
        return {"success": False, "message": response.status_code, "data": None}


def abilityLookup(ability=""):
    if ability == "":
        return {"success": False, "message": 400, "data": None}
    response = requests.get("https://pokeapi.co/api/v2/ability/" + ability)
    if response.status_code == 200:
        data = response.json()
        # parse data
        parsed_data = ""
        for item in data["effect_entries"]:
            if item["language"]["name"] == "en":
                parsed_data = item["effect"]
        return {"success": True, "message": "success", "data": parsed_data}
    else:
        return {"success": False, "message": response.status_code, "data": None}


def poketypes(poketype):
    response = requests.get("https://pokeapi.co/api/v2/type/" + str(poketypetonum(poketype)))
    if response.status_code == 200 and poketype !=- -1:
        data = response.json()
        return {
            "success": True,
            "message": "success",
            "data": data['damage_relations']
        }
    else:
        return {"success": False, "message": response.status_code, "data": None}

def poketypetonum(poketype):
    if poketype == "normal":
        return 1
    if poketype == "fighting":
        return 2
    if poketype == "flying":
        return 3
    if poketype == "poison":
        return 4
    if poketype == "ground":
        return 5
    if poketype == "rock":
        return 6
    if poketype == "bug":
        return 7
    if poketype == "ghost":
        return 8
    if poketype == "steel":
        return 9
    if poketype == "fire":
        return 10
    if poketype == "water":
        return 11
    if poketype == "grass":
        return 12
    if poketype == "electric":
        return 13
    if poketype == "psychic":
        return 14
    if poketype == "ice":
        return 15
    if poketype == "dragon":
        return 16
    if poketype == "dark":
        return 17
    if poketype == "fairy":
        return 18
    return -1 
