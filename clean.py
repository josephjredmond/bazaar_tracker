#https://api.hypixel.net/v2/skyblock/bazaar

import os
import json

path = "./data/"

if not os.path.exists("data"):
    print("No data folder found. Run api_fetch.py first.")
    exit(1)

if not os.path.exists("cleaned"):
    os.makedirs("cleaned")

files = os.listdir(path)

for file_path in files:
    if file_path.endswith(".json"): 
        with open(path + file_path, "r") as file:
            bazaar_data = json.load(file)
            
        #os.remove(file) 

        # Find items with no sell volume
        unused_items = [] 
        for item in bazaar_data["products"]:
            sellVolume = bazaar_data["products"][item]["quick_status"]["sellVolume"]
            if sellVolume == 0:
                #print(item, sellVolume)
                unused_items.append(item)

        # Remove items with no sell volume
        for item in unused_items:
            #del get_bazaar_data()["products"][item]
            bazaar_data["products"].pop(item)


        # Save cleaned data
        with open("./cleaned/"+ file_path, "w") as file:
            json.dump(bazaar_data, file)