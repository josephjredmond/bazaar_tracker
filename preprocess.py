import numpy as np
import pandas as pd
import time
import os
import json

def process():
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists('preprocessed'):
        os.makedirs('preprocessed')

    # get all the files in the data folder
    data_files = os.listdir('data')
    data_files = [f for f in data_files if f.endswith('.json')]

    cols = ['Date', 'item', 'sell_price', 'sell_volume', 'sell_moving_week', 'sell_orders', 'buy_price', 'buy_volume', 'buy_moving_week', 'buy_orders', 'max_sell_price', 'min_buy_price']

    # pre allocate memory for the data
    organised_data = np.zeros(shape = (3000*len(data_files), len(cols)))

    unique_items = []
    index = 0

    for file_path in data_files:

        # load the data from the file
        data = ""
        with open(f'data/{file_path}', 'r') as f:
            data = json.load(f)

        # Extract date from data 
        recorded = int(data["lastUpdated"]/1000) 

        for product in data["products"]: 
            index += 1

            # quick_status
            quick_status = data["products"][product]["quick_status"] 
            item = quick_status["productId"]
            item = item.replace(":", "-")
            sell_price = quick_status["sellPrice"]
            sell_volume = quick_status["sellVolume"]
            sell_moving_week = quick_status["sellMovingWeek"]
            sell_orders = quick_status["sellOrders"]
            buy_price = quick_status["buyPrice"]
            buy_volume = quick_status["buyVolume"]
            buy_moving_week = quick_status["buyMovingWeek"]
            buy_orders = quick_status["buyOrders"]

            # sell_summary - Get the maximum sell price
            sell_summary = data["products"][product]["sell_summary"]

            max_sell_price = 0
            for sell in sell_summary:
                if sell["pricePerUnit"] > max_sell_price:
                    max_sell_price = sell["pricePerUnit"]

            # buy_summary - Get the minimum buy price
            buy_summary = data["products"][product]["buy_summary"]

            min_buy_price = 999999999
            for buy in buy_summary:
                if buy["pricePerUnit"] < min_buy_price:
                    min_buy_price = buy["pricePerUnit"]
            if min_buy_price == 999999999:
                min_buy_price = 0


            if item not in unique_items:
                unique_items.append(item)

            # Convert item to unique integer id to store in np array
            uid = unique_items.index(item)  
            organised_data[index] = [recorded, uid, sell_price, sell_volume, sell_moving_week, sell_orders, buy_price, buy_volume, buy_moving_week, buy_orders, max_sell_price, min_buy_price]

    # Remove left over rows
    organised_data = organised_data[organised_data[:,0] != 0]

    # Loop through all the unique items and save them to a csv file
    for i in range(len(unique_items)):
        item = unique_items[i] 

        # Extract only the data for the current item
        item_data = organised_data[organised_data[:,1] == i] 

        # Sort by date
        item_data = item_data[item_data[:,0].argsort()]

        # Convert to pandas dataframe & remove the item column
        df = pd.DataFrame(item_data, columns=cols)
        df = df.drop(columns=['item'])  

        # Convert Date col from unix timestamp to YYYY-MM-DD-HH
        df["Date"] = df["Date"].apply(lambda x: time.strftime('%Y-%m-%d-%H', time.localtime(x))) 

        # Check if the item file already exists
        if os.path.exists(f'preprocessed/{item}.csv'):
            # Load the old data
            old_df = pd.read_csv(f'preprocessed/{item}.csv')  

            # Check if the new data is already in the old data
            new_rows = df[~df["Date"].isin(old_df["Date"])]

            # Append the new data to the old data
            old_df = pd.concat([old_df, new_rows], ignore_index=True)

            # Save the new data
            old_df.to_csv(f'preprocessed/{item}.csv', index=False)
        else: # Otherwise
            # Save the new data
            df.to_csv(f'preprocessed/{item}.csv', index=False)

def load_data():
    data_files = os.listdir('preprocessed')
    data_files = [f for f in data_files if f.endswith('.csv')]

    data = {}
    for file_path in data_files:
        df = pd.read_csv(f'preprocessed/{file_path}')
        data[file_path.replace('.csv', '')] = df

    return data

if __name__ == "__main__":
    process()