import json
import csv

#Read the file list from a csv file and invoke the function for each file
def read_file_list(file_path):
    file_list = []
    try:
        with open(file_path
                    , 'r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 1:
                        file_list.append(row[0])
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    return file_list

#Open a JSON file and return the data
def open_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

#Update the drop shadow in the JSON file
def update_drop_shadow(data):
    drop_shadow = data.get('visual', {}).get('visualContainerObjects', {}).get('dropShadow', [])
    for item in drop_shadow:
        if item.get('properties', {}).get('show', {}).get('expr', {}).get('Literal', {}).get('Value') == "false":
            item['properties']['show']['expr']['Literal']['Value'] = "true"
            item['properties']['transparency'] = {
                "expr": {
                    "Literal": {
                        "Value": "20D"
                    }
                }
            }
    return data

#Save the data to a JSON file
def save_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

#Example usage--------------------------------------------------------------
#Define the path to the CSV file which contains the list of files (generate the list with the findfiles.py script)
csv_file_path = r'find files script output file path'
file_list = read_file_list(csv_file_path)
#---------------------------------------------------------------------------

#Iterate through the list of files and update the drop shadow
for json_file_path in file_list:
    if not json_file_path.lower().endswith('visual.json'):
        print(f"Skipping non-JSON file: {json_file_path}")
        continue
    data = open_json_file(json_file_path)
    updated_data = update_drop_shadow(data)
    save_json_file(json_file_path, updated_data)
    print(f"Updated dropshadow for {json_file_path}")