import os
import pandas as pd
import json

#Input Parameters----------------------------------------------------------------------------------------------------------------
#Define the root directory of the report
root_directory = r'report folder path'
#Define the location where the file will be saved
save_location = r'save location'
#Define the name of the saved file
file_name = 'saved_file_name.csv'

#Functions
def get_paths(root_dir):
    paths = []
    root_dir = os.path.abspath(root_dir)  # Ensure the root directory is an absolute path
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            # print(full_path)
            # Remove the root directory part from the full path
            relative_path = os.path.relpath(full_path, root_dir)
            path_components = relative_path.split(os.sep)
            paths.append(path_components)
    return paths

def create_dataframe_from_paths(paths):
    # Determine the maximum depth of the directory structure
    max_depth = max(len(path) for path in paths)
    
    # Create column names based on the maximum depth
    columns = [f'Level_{i}' for i in range(max_depth)]
    
    # Create the DataFrame
    df = pd.DataFrame(paths, columns=columns)
    
    return df

def get_display_name_from_json(json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data.get('displayName', None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def get_visual_type_from_json(json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            title = data.get('visual', {}).get('visualContainerObjects', {}).get('title', [])
            first_title = title[0] if isinstance(title, list) and len(title) > 0 else {}
            title_result = first_title.get('properties', {}).get('text', {}).get('expr', {}).get('Literal', {}).get('Value', None)        
            visual_type = data.get('visual', {}).get('visualType', None)
            if(title_result == None):
                title_result = data.get('visualGroup', {}).get('displayName', 'Not found')
            if(visual_type == None):
                visual_type = 'Visual Group'
            return visual_type, title_result
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    
# Save the DataFrame to a CSV file or print it
def save_dataframe(df, file_path):
    df.to_csv(file_path, index=False)



# Example usage
print("Extracting files from the report...")
print(root_directory)
paths = get_paths(root_directory)
df = create_dataframe_from_paths(paths)
copy = df.copy()
#how many rows are in the dataframe
print(len(df), " files extracted from the report")

# Add a new column for display_name
copy['page_name'] = None
copy['visual_name'] = None
copy['visual_type'] = None

# Populate the display_name column
for index, row in df.iterrows():
    if row.get('Level_1') == 'bookmarks':
        json_path = os.path.join(root_directory, *row.dropna())
        display_name = get_display_name_from_json(json_path)
        if display_name is not None:
            copy.at[index, 'page_name'] = display_name

    if row.get('Level_3') == 'visuals':
        json_path = os.path.join(root_directory, *row.dropna())
        result = get_visual_type_from_json(json_path)
        if result is not None:
            visual_type, visual_name = result
            copy.at[index, 'visual_type'] = visual_type
            copy.at[index, 'visual_name'] = visual_name      

    if row.get('Level_3') == 'page.json':
        json_path = os.path.join(root_directory, *row.dropna())
        display_name = get_display_name_from_json(json_path)
        if display_name is not None:
            copy.loc[df['Level_2'] == row['Level_2'], 'page_name'] = display_name
            



#Save file
save_dataframe(copy, os.path.join(save_location, file_name))