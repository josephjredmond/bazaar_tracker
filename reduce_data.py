#https://api.hypixel.net/v2/skyblock/bazaar

import json 
import os

data_path = "./cleaned/"
save_path = "./reduced/"

if not os.path.exists("cleaned"):
    print("No cleaned folder found. Run clean.py first.")
    exit(1)

bazaar_folder = os.listdir(data_path)

shrink = 5

for path in bazaar_folder:
    if not path.endswith('.json'):
        continue

    # open the file
    with open( data_path + path, "r") as file: 
        data = json.load(file) 

        products = data["products"].copy() # Copy the JSON object to avoid modifying the original object while iterating over it
        
        for product in products:
            # Remove items with no sell volume
            if "quick_status" in data["products"][product]:
                if data["products"][product]["quick_status"]["sellVolume"] == 0:
                    data["products"].pop(product)
                    continue


            # Sort buy_summary by pricePerUnit and keep only the first X entries 
            if "buy_summary" in data["products"][product]:
                entries = data["products"][product]["buy_summary"]

                # Only if there are more than X entries
                if len(entries) > shrink:
                    entries.sort(key=lambda x: x["pricePerUnit"]) # sort by pricePerUnit
                    # want only the first items in the list with the best 'selling' price
                    data["products"][product]["buy_summary"] = entries[:shrink]

            # Sort sell_summary by pricePerUnit and keep only the last X entries 
            if "sell_summary" in data["products"][product]: 
                entries = data["products"][product]["sell_summary"]
                
                if len(entries) > shrink:
                    entries.sort(key=lambda x: x["pricePerUnit"])
                    # want only the last items in the list with the best 'buying' price
                    data["products"][product]["sell_summary"] = entries[-shrink:]
            


        with open(save_path + path + ".json", "w") as file:
            json.dump(data, file)