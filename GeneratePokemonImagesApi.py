from PIL import Image
import os
import pandas as pd
import time
from huggingface_hub.inference_api import InferenceApi

from dotenv import load_dotenv
load_dotenv()

def create_pokemon_image(pokemon_info=None):
    inference = InferenceApi(repo_id="black-forest-labs/FLUX.1-schnell", token=os.getenv("HUGGINF_FACE_KEY"))

    folder_name = os.path.dirname(os.path.abspath(__file__))

    pokemon_data = pd.read_csv(folder_name + "/Data/PokemonData/new_pokemon.csv")

    if pokemon_info is None:
        pokemon_data = pd.read_csv(folder_name + "/Data/PokemonData/new_pokemon.csv")
    else:
        pokemon_data = pokemon_info

    for index, row in pokemon_data.iterrows():
        
        file_name = folder_name + "/Data/PokemonData/NewPokemonImages/" + row["PokemonName"] + ".png"
        
        if not os.path.exists(file_name):
            start_time = time.time()
            prompt = "Create a Pokemon called " + row["PokemonName"] + ". " + row["Description"]
            image = inference(inputs=prompt)
    
            image.save(file_name)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"To generate {row["PokemonName"]}: time elapsed is {elapsed_time} seconds")