import pandas as pd
import xml.etree.ElementTree as ET
import os

folder_path = os.path.dirname(os.path.abspath(__file__))

def get_info_from_files():

    # Get absolute path so we can execute this file from anywhere
    xmls_folder = folder_path + "/Data/PokemonData/TableData"
    list_roots = []

    # Get all xmls in the folder and save them as trees
    for XmlFile in os.listdir(xmls_folder):
        tree = ET.parse(xmls_folder + "/" + XmlFile)
        root = tree.getroot()
        list_roots.append({
            "name": os.path.splitext(XmlFile)[0],
            "val": root
        })
        
    # Transform trees into dict structures
    def parse_xml(root):
        data = []
        for child in root:
            entry = {}
            for subchild in child:
                entry[subchild.tag] = subchild.text
            data.append(entry)
        return data

    list_data = {}

    # Get dict structures and save them into pandas (not needed, just to use pandas that is more efficient)
    for root in list_roots:
        data = parse_xml(root["val"])
        list_data[root["name"]] = data

    return list_data

def get_info_from_csv():
    csv_file = folder_path + "/Data/PokemonData/Pokemon_2.csv"
    df = pd.read_csv(csv_file)
    
    df["PokemonName"] = df["Name"] + " " + df["Form"]
    
    #Modify columns to have a similar structure than the other table
    wanted_cols ={
        "PokemonName": "PokemonName",
        "HP": "Health",
        "Attack": "Attack",
        "Defense": "Defense",
        "Sp. Atk": "SpecialAttack",
        "Sp. Def": "SpecialDefense",
        "Speed": "Speed",
        "Type1": "Type1",
        "Type2": "Type2"
    }
    
    final_df = df[list(wanted_cols.keys())].rename(columns=wanted_cols)
    
    list_data = {"Pokemon": final_df.to_dict(orient='records')}
    
    return list_data

def get_info_from_csv_2():
    csv_file = folder_path + "/Data/PokemonData/Pokemon_3.csv"
    df = pd.read_csv(csv_file)
    
    df["PokemonName"] = df["name"].apply(lambda x: x.capitalize())
    
    df['Id'] = range(0, len(df))
    df["Normal"] = True
    
    #Modify columns to have a similar structure than the other table
    wanted_cols ={
        "Id": "Id",
        "index": "Index",
        "PokemonName": "PokemonName",
        "hp": "Health",
        "atk": "Attack",
        "def": "Defense",
        "spatk": "SpecialAttack",
        "spdef": "SpecialDefense",
        "speed": "Speed",
        "type1": "Type1",
        "type2": "Type2",
        "desc": "Description",
        "Normal": "Normal"
    }
    
    final_df = df[list(wanted_cols.keys())].rename(columns=wanted_cols)
    
    list_data = {"Pokemon": final_df.to_dict(orient='records')}
    
    return list_data

def get_info_from_csv_new():
    csv_file = folder_path + "/Data/PokemonData/new_pokemon.csv"
    df = pd.read_csv(csv_file)
    
    df["New"] = True
    
    df['Id'] = range(0, len(df))
    
    list_data = {"Pokemon": df.to_dict(orient='records')}
    
    return list_data