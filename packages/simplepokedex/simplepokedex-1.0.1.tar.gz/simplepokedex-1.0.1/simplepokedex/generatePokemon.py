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
