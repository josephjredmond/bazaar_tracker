import os
import json

product = "ENCHANTMENT_PROTECTION_1"

with open('processed/bazaar_2024_02_15_06_00_51.json', 'r') as f:
    data = json.load(f)

    products = data['products']

    print(product)
    print(products[product]["quick_status"]) 


with open('data/file.json', 'r') as f:
    data = json.load(f)

    products = data['products']

    print(product)
    print(products[product]["quick_status"])
    
    # for product in products:
    #     print(product)
    #     print(products[product]["quick_status"])