#https://api.hypixel.net/v2/skyblock/bazaar

from preprocess import process_db
import requests
import json
import time
import os

if not os.path.exists("data"): 
    os.makedirs("data")

# Fetch market data from API
response = requests.get("https://api.hypixel.net/skyblock/bazaar")


if response.status_code == 200: # if the request was successful
    data = response.json() # JSONify the data


    #convert epoch to YYYY_MM_DD HH_MM_SS
    date = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(data["lastUpdated"]/1000))
    with open("./data/bazaar_" + date + ".json", "w") as file:
        json.dump(data, file)

    process_db() 