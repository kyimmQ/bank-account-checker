import unicodedata
def vietnamese_to_lower(name: str):
    name = name.strip()
    # Normalize the string to decompose accented characters
    name = unicodedata.normalize('NFD', name)
    # Remove the diacritical marks (accents)
    name_char = [char for char in name if unicodedata.category(char) != 'Mn']
    for i in range(len(name_char)):
        if name_char[i] == "Đ" or name_char[i] == "đ":
            name_char[i] = "d" 
    name = ''.join(name_char)
    # Convert the name to lowercase
    return name.lower()

# Function to handle fully uppercase names
def uppercase_to_lower(name):
    # Simply convert the uppercase name to lowercase
    return name.lower()