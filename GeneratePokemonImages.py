import torch
import os
from diffusers import FluxPipeline
import pandas as pd
import time

def create_pokemon_image(pokemon_info=None):
    start_time = time.time()

    folder_name = os.path.dirname(os.path.abspath(__file__))

    device = torch.device("cpu")

    pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16).to(device)
    #pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

    if pokemon_info is None:
        pokemon_data = pd.read_csv(folder_name + "/Data/PokemonData/new_pokemon.csv")
    else:
        pokemon_data = pokemon_info

    for index, row in pokemon_data.iterrows():
        print(row["PokemonName"])

        prompt = "Create a Pokemon called " + row["PokemonName"] + ". " + row["Description"]
        image = pipe(
            prompt,
            guidance_scale=0.0,
            num_inference_steps=4,
            max_sequence_length=256,
            generator=torch.Generator("cpu").manual_seed(0)
        ).images[0]

        file_name = folder_name + "/Data/PokemonData/NewPokemonImages/" + row["PokemonName"] + ".png"

        image.save(file_name)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"To generate {row["PokemonName"]}: time elapsed is {elapsed_time} seconds")
        
create_pokemon_image()