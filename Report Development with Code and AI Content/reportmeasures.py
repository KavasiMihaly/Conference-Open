import json
import csv

# Extract information from the JSON file
def extract_information(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Print the structure of the JSON data for debugging
    # print("JSON data structure:", type(data))
    # if isinstance(data, dict):
    #     print("Keys in the dictionary:", data.keys())
    
    extracted_info = []
    
    entities = data.get('entities', [])
    for entity_data in entities:
        entity_name = entity_data.get('name', '')
        if isinstance(entity_data, dict):
            measures = entity_data.get('measures', [])
            for measure in measures:
                info = {}
                info['entity'] = entity_name
                info['measure_name'] = measure.get('name', '')
                info['expression'] = measure.get('expression', '')
                info['dataType'] = measure.get('dataType', '')
                info['formatString'] = measure.get('formatString', '')
                info['display_folder'] = measure.get('displayFolder', '')
                extracted_info.append(info)
        else:
            print(f"Unexpected entity data type: {type(entity_data)}")
    
    return extracted_info

def save_to_csv(extracted_info, output_file_path):
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['entity','display_folder', 'measure_name', 'expression', 'dataType', 'formatString'], quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for info in extracted_info:
            # Remove leading and trailing whitespace from each value
            cleaned_info = {key: value.strip() if isinstance(value, str) else value for key, value in info.items()}
            writer.writerow(cleaned_info)

# Example usage---------------------------------------------------
#Define the location of the report extensions file and the output file
json_file_path = r'reportextensions.json file location'
output_file_path = r'save file location and name'

extracted_info = extract_information(json_file_path)
save_to_csv(extracted_info, output_file_path)

print(f"Extracted report measure information saved to {output_file_path}")