from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import Levenshtein

def fuzzy_search_pokemon(pokemon_list, pokemon_name, ratio = 0.5):
    similar_pokemon = []
    
    pokemon_name = pokemon_name.lower()
    
    for pokemon in pokemon_list:
        pokemon_name_str = pokemon["PokemonName"].lower()
        max_fuzz_ratio = 0
        
        # Generar todas las subcadenas posibles
        for i in range(len(pokemon_name_str)):
            for j in range(i + 1, len(pokemon_name_str) + 1):
                substring = pokemon_name_str[i:j]
                fuzz_ratio = fuzz.ratio(substring, pokemon_name)
                print(f"Comparando '{substring}' con '{pokemon_name}': ratio = {fuzz_ratio}")
                max_fuzz_ratio = max(max_fuzz_ratio, fuzz_ratio)
        
        if max_fuzz_ratio >= (ratio * 100):
            new_pokemon = pokemon
            new_pokemon["ratio"] = max_fuzz_ratio
            similar_pokemon.append(pokemon)
            
    similar_pokemon = sorted(similar_pokemon, key=lambda x: x["ratio"], reverse=True)
            
    return similar_pokemon

def fuzzy_search_pokemon_one(pokemon_list, pokemon_name):
    names = [pokemon["PokemonName"] for pokemon in pokemon_list]
    best_match, score = process.extractOne(pokemon_name, names, scorer=process.fuzz.ratio)

    # Buscamos el diccionario completo correspondiente al mejor nombre
    for pokemon in pokemon_list:
        if pokemon["PokemonName"] == best_match:
            return pokemon
    return None

def search_word(pokemon_list, pokemon_name, ratio = 0.5):
    matching_words = []
    
    search_term = pokemon_name.lower()
    for word in pokemon_list:
        word_lower = word['PokemonName'].lower()
        
        if (search_term in word_lower):
            # If the search term is contained in any field, add it with a high score
            word["similarity_score"] = 1.0
            matching_words.append(word)
        else:
            # Calculate similarity for subwords of the same length as the search term
            for field in [word_lower]:
                for i in range(len(field) - len(search_term) + 1):
                    subword = field[i:i+len(search_term)]
                    #similarity_score = calculate_similarity(search_term, subword)
                    similarity_score = Levenshtein.ratio(search_term, subword)
                    if similarity_score > ratio:  # Adjust this threshold as needed
                        word["similarity_score"] = similarity_score
                        matching_words.append(word)
                        break  # Only add the word once with its highest similarity score
                if matching_words and matching_words[-1] == word:
                    break  # Stop checking other fields if we've already added this word
    
    # Sort by similarity score, highest first
    matching_words.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return matching_words
    
def calculate_similarity(s1, s2):
    # Simple Levenshtein distance-based similarity
    m = len(s1)
    n = len(s2)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    
    max_len = max(m, n)
    return 1 - (d[m][n] / max_len)