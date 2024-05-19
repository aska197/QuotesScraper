import os

# Specify the paths to your JSON files
json_files = ['quotes.json', 'authors.json']

# Clear the contents of each file
for file in json_files:
    if os.path.exists(file):
        with open(file, 'w') as f:
            f.write('')
