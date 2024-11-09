
def get_pokemon_types(pokemon, all_data):
    types = all_data["Types"]
    print(types)
    type1 = types[int(pokemon["Type1_Id"])-1]["TypeName"]
    type2 = types[int(pokemon["Type2_Id"])-1]["TypeName"]
    
    return type1, type2