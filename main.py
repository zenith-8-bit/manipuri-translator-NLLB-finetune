from rapidfuzz import process  # Recommend RapidFuzz for its speed and license friendliness

# Example dictionary of Manipuri words to English translations
manipuri_dict = {
    "numit": "day",
    "sanakh": "time",
    "ming": "name",
    # Add more entries as needed
}

def get_translation(input_word, dictionary, threshold=80):
    # Try direct lookup first
    if input_word in dictionary:
        return dictionary[input_word]
    
    # Fuzzy matching if direct match fails
    match, score, _ = process.extractOne(input_word, dictionary.keys())
    if score >= threshold:
        return dictionary[match]
    else:
        return None

# Example usage
user_input = "numiiiiiit"  # Example misspelled input
translation = get_translation(user_input.lower(), manipuri_dict)
if translation:
    print(f"The translation for '{user_input}' is '{translation}'.")
else:
    print(f"Could not find a close match for '{user_input}'.")
