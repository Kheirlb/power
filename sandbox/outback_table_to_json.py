import sys
import pandas as pd

# Validate input.
# TODO(kparks): Use argparse.
if len(sys.argv) <= 1:
  print(".csv file required")
  sys.exit(1)
file = sys.argv[1]
if not file.endswith(".csv"):
  print("must end with .csv")
  sys.exit(1)

df = pd.read_csv(file)
# print(df.info())

SF_TYPE = "sunssf"

points = []
track_sf = set()

support_types = {"uint16", "int16", "string", "uint32"}

for index, row in df.iterrows():
    did = row["DID"]
    start = row["Start"]
    end = row["End"]
    size = row["Size"]
    name = row["Name"]
    
    # Fix name import issues:
    name = name.replace(" ", "")
    name = name.replace("\n","")
    if name.startswith("R/W"):
        name = name.replace("R/W","")

    data_type = row["Type"]
    units = row["Units"]
    sf = row["Scale Factor"]
    contents = row["Contents"]
    description = row["Description"]
    
    # Validate type.
    # Handle 'string (14)' case.
    if "string" in data_type:
        data_type = "string"
    if data_type not in support_types:
        print("encountered unsupport type:", data_type)
        sys.exit(1)

    # Check units type and handle special types.
    if isinstance(units, str):
        if "Enumerated" in units:
            data_type = "enum16"
            
        if "Address" in units:
            data_type = "ipaddr"
            
        if "Bitfield" in units:
            data_type = "bitfield16"

    point = {
        "label": name,
        "desc": description,
        "mandatory": "M",
        "name": name,
        "size": size,
        "type": data_type
    }
    if isinstance(sf, str):
        track_sf.add(sf)
        point["sf"] = sf
        # print(sf) 
        
    points.append(point)
    # print(name)

# print(track_sf)

import json

data = {}
model_name = f"model_{did}"
data.update({
    "group": {
        "label": "TBD",
        "name": model_name,
        "points": points,
        "type": "group"
    },
    "id": did
})

with open(f'{model_name}.json', 'w') as fp:
    json.dump(data, fp, indent=4)
