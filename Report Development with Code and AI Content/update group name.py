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

# Modify the display name in the json file
def modify_display_name(json_file_path, modified_value, replaced_value):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    def update_display_name(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'displayName' and isinstance(value, str):
                    if replaced_value is not None and replaced_value in value:
                        obj[key] = value.replace(replaced_value, modified_value)
                    else:
                        obj[key] = value + ' ' +modified_value
                else:
                    update_display_name(value)
        elif isinstance(obj, list):
            for item in obj:
                update_display_name(item)
    
    update_display_name(data)
    
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

#Example usage--------------------------------------------------------------
#Add the file path of the csv file containing the list of files to be modified (generate the file using the find_files.py script)
csv_file_path = r'C:\Users\kavas\OneDrive\Documents\GitHub\Python-Scripts\Save Files\matching_files_visualGroup_20241119.csv'
#Add the value to be replaced or added to the display name
replace = None
modify_with = "group"
#---------------------------------------------------------------------------

file_list = read_file_list(csv_file_path)

for json_file_path in file_list:
    if not json_file_path.lower().endswith('.json'):
        print(f"Skipping non-JSON file: {json_file_path}")
        continue
    modify_display_name(json_file_path, modify_with, replace)
    print(f"Updated displayName values in {json_file_path}")

# json_file_path = r'C:\Users\mihaly.kavasi\OneDrive - Avanade\Projects\Page\MWM\Leadership Insights Mihaly.Report\definition\pages\2857ff8ac39432eb67aa\visuals\6d46a36c7689a92b1616\visual.json'
# modify_display_name(json_file_path)
# print(f"Updated displayName values in {json_file_path}")