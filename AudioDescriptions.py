from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch
import os
import pandas as pd
import time

def create_pokemon_audio(pokemon_info=None):
    synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    folder_name = os.path.dirname(os.path.abspath(__file__))

    if pokemon_info is None:
        pokemon_data = pd.read_csv(folder_name + "/Data/PokemonData/new_pokemon.csv")
    else:
        pokemon_data = pokemon_info

    for index, row in pokemon_data.iterrows():
        
        file_name = folder_name + "/Data/PokemonData/DescriptionAudios/" + row["PokemonName"] + ".wav"
        
        if not os.path.exists(file_name):
            start_time = time.time()
            print("Starting description of " + row["PokemonName"])
            desc = row["Description"]
            # This speech model only accepts descriptions of equal or less tahn 598 characters
            if len(desc) > 598:
                desc = desc[:598]
            speech = synthesiser(desc, forward_params={"speaker_embeddings": speaker_embedding})
            sf.write(file_name, speech["audio"], samplerate=speech["sampling_rate"])
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"To generate {row["PokemonName"]}: time elapsed is {elapsed_time} seconds")