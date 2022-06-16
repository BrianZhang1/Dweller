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


    def create_default_data(self, bg_size, tile_size):
        data = {
            "maps": []
        }
        cols = int(bg_size[0]/tile_size) + 1
        rows = int(bg_size[1]/tile_size) + 1

        defaultmap = {
            "name": "default",
            "tilemap": [],
            "width": 1
        }
        samplemap = {
            "name": "sample",
            "tilemap": [],
            "width": 1
        }

        defaulttilemap = []
        for i in range(cols):
            col = []
            for k in range(rows):
                if k == rows-1:
                    col.append(1)
                else:
                    col.append(0)
            defaulttilemap.append(col)
        defaultmap["tilemap"] = defaulttilemap
        data["maps"].append(defaultmap)

        sampletilemap = []
        for i in range(cols):
            col = []
            for k in range(rows):
                if k == rows-1:
                    col.append(1)
                elif i == 1 and k == rows-4:
                    col.append(1)
                elif (k == rows-4 or k == rows-3 or k == rows-2) and i in [6, 7, 8]:
                    col.append(1)
                elif k == rows-5 and i in [12, 13, 14, 15]:
                    col.append(1)
                else:
                    col.append(0)
            sampletilemap.append(col)
        samplemap["tilemap"] = sampletilemap
        data["maps"].append(samplemap)

        with open(DATA_PATH, "w") as json_file:
            json.dump(data, json_file)
        
        self.data = data

        return 0


    def save_map(self, name, map, width):
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
            "width": width
        }

        self.data["maps"].append(map)
        self.write_data()

        return 0
