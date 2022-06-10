import json

DATA_PATH = "data.json"
INIT_DATA = {
    "maps": []
}


# loads and returns data
def load_data():
    try:
        with open(DATA_PATH) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        with open(DATA_PATH, "w") as json_file:
            json.dump(INIT_DATA, json_file)
            data = INIT_DATA
    
    return data
