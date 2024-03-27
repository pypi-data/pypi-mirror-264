import requests

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
