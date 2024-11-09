from CreatePokemonInformation import create_new_pokemon_information
from GeneratePokemonImagesApi import create_pokemon_image
from AudioDescriptions import create_pokemon_audio
import pandas as pd

def generate_pokemon(amount=0):
    if amount > 0:
        pokemon = create_new_pokemon_information(amount)
        print(pokemon)
        df = pd.DataFrame(pokemon, columns=['PokemonName', 'Description', 'Type1', 'Type2', 'Health', 'Attack', 'Defense', 'SpecialAttack', 'SpecialDefense', 'Speed'])
        create_pokemon_image(df)
        create_pokemon_audio(df)
    else:
        create_new_pokemon_information(1)
        create_pokemon_image()
        create_pokemon_audio()
        
generate_pokemon()
    