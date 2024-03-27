import requests


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
