import json

DATA_PATH = "data.json"

class DataHandler:
    def __init__(self):
        self.data = None


    # loads and returns data
    def load_data(self):
        try:
            with open(DATA_PATH) as json_file:
                data = json.load(json_file)
                self.data = data
                return 0
        except FileNotFoundError:
            return 1


    def write_data(self, data=None):
        if data == None:
            data = self.data
        with open(DATA_PATH, "w") as json_file:
            json.dump(data, json_file)


    def create_default_data(self):
        with open("default_data.json") as default_data:
            data = json.load(default_data)

        with open(DATA_PATH, "w") as json_file:
            json.dump(data, json_file)
        
        self.data = data

        return 0


    def save_map(self, name, map):
        # first, check for errors with name
        # check for empty name
        if len(name) == 0:
            return "Name Empty."
        # check for duplicate name
        for data_map in self.data["maps"]:
            if data_map["name"] == name:
                return "Duplicate Name."

        # transform map into list with tile types
        new_tilemap = []
        for col in map.tilemap:
            new_col = []
            for tile in col:
                new_col.append(tile.type)
            new_tilemap.append(new_col)
        
        map = {
            "name": name,
            "tilemap": new_tilemap,
            "width": map.width
        }

        self.data["maps"].append(map)
        self.write_data()

        return 0
