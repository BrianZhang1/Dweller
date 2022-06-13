import json

DATA_PATH = "data.json"


# loads and returns data
def load_data(bg_size, tile_size):
    try:
        with open(DATA_PATH) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        with open(DATA_PATH, "w") as json_file:
            default_data = create_default_data(bg_size, tile_size)
            json.dump(default_data, json_file)
            data = default_data
    
    return data


def create_default_data(bg_size, tile_size):
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

    return data


def save_map(name, map):
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
        "width": 1
    }

    # WRITE TO FILE
