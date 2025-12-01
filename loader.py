import gzip
import json
from collections import defaultdict

def readGz(path):
    # Open in text mode ('rt') with UTF-8 encoding for JSON lines
    path = "datasets2/" + path
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for l in f:
            # Safely parse each line as JSON
            yield json.loads(l)

def load_to_dict(file_to_read):
    data = []
    try:
        for item in readGz(file_to_read):
            data.append(item)
    except EOFError as e:
        # Catching the specific EOFError indicating a corrupted file
        print(f"EOFError: Compressed file '{file_to_read}' ended prematurely. Error: {e}")
        print(f"This often indicates a corrupted or incomplete gzip file. Successfully loaded {len(data)} items before the error.")
    except Exception as e:
        # Catching other potential errors during decompression or JSON parsing
        print(f"An unexpected error occurred while reading '{file_to_read}': {e}")
        print(f"Successfully loaded {len(data)} items before the error.")
    return data

def save_likes(filename, data_dict):
    filename = "eval/"+filename
    with open(filename, "w") as fp:
        json.dump(data_dict, fp, indent=4)
    print("Saved to ", filename)

def load_user_likes(filename):
    """
    Load a user_likes JSON file back into a dict[user_id] = list of liked places.
    """
    #filename = "eval/"+filename
    with open(filename, "r") as f:
        data = json.load(f)

    # Ensure values are lists, not sets or other types
    return {user_id: list(likes) for user_id, likes in data.items()}
