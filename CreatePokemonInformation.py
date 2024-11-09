import torch
from transformers import pipeline
import csv
import random
import string
import os
import unidecode
import time
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

# Get the model
token = os.getenv("HUGGINF_FACE_KEY")
model_id = "meta-llama/Llama-3.2-1B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    token=token
    )

def create_new_pokemon_information(amount):
    final_pokemon = []
    file_name = os.path.dirname(os.path.abspath(__file__)) + "/Data/PokemonData/new_pokemon.csv"
    current_pokemon = pd.read_csv(file_name)
    
    for i in range(amount):
        start_time = time.time()

        # Generate basic data for the Pókemon
        # The seed to create the name
        seed = ''.join(random.choices(string.ascii_letters, k=30))

        # Select the base stats for the pokemon
        health = random.randint(1,250)
        attack = random.randint(1,250)
        defense = random.randint(1,250)
        s_attack = random.randint(1,250)
        s_defense = random.randint(1,250)
        speed = random.randint(1,250)

        # Select a random typing
        possible_types = ["Normal", "Fire", "Fighting", "Water", "Flying", "Grass", "Poison", "Electric", 
                            "Ground", "Psychic", "Rock", "Ice", "Bug", "Dragon", "Ghost", "Dark", "Steel", "Fairy"]

        random_type1 = random.choice(possible_types)
        random_type2 = random.choice(possible_types)
        random_type2_add = ""

        # Possibility of a 5% to have a 1 type pokemon
        if random.randint(0,100) <= 10:
            random_type2_add = ""
        else:
            random_type2_add = " and " + random_type2


        # Generate the name of the new pokémon using a random typing
        messages = [
            {"role": "system", "content": "You are an expert in creating names for new Pokémon. You will only awnser with one word of a maximum of 15 characters. No description or extra information will be given."},
            {"role": "user", "content": "Give a name to a new Pókemon with a typing of " + random_type1 + random_type2_add + ". Use some of this letters for the name: " + seed.lower()},
        ]
        outputs = pipe(
            messages,
            max_new_tokens=256,
        )
        pokemon_name = outputs[0]["generated_text"][-1]["content"]
        
        if pokemon_name in current_pokemon["PokemonName"]:
            print("Pokemon " + pokemon_name + " already exists")
            continue

        # Generate a description for the newly created pokémon
        messages = [
            {"role": "system", "content": "You are an expert in creating descriptions for new Pokémon. Just answer with a medium size description, no extra information."},
            {"role": "user", "content": "Give a description to a new Pókemon with a typing of " + random_type1 + random_type2 + " and the name " + pokemon_name},
        ]
        outputs = pipe(
            messages,
            max_new_tokens=256,
        )
        pokemon_desc = unidecode.unidecode(outputs[0]["generated_text"][-1]["content"])

        # Save the information in a csv

        data = [pokemon_name, pokemon_desc, random_type1, random_type2, health, attack, defense, s_attack, s_defense, speed]
        
        final_pokemon.append(data)

        with open(file_name, mode='a', newline='') as file:
            escritor_csv = csv.writer(file)
            escritor_csv.writerows([data])
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"To generate {pokemon_name}: time elapsed is {elapsed_time} seconds")
        
    return final_pokemon