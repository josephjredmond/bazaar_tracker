import os
import json

from preprocess import process_db

files = os.listdir('./processed')

files = [file for file in files if file.endswith('.json')]
files.sort()

for file in files:
    print(file)