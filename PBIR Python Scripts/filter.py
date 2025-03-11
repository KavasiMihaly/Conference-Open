import os
import pandas as pd
import json

#Parameters
root_directory = r'insert report folder path here'
save_location = r'insert save location here'
file_name = 'folder_structure_filter.csv'
filter_word = 'visuals'

#Functions
def get_paths(root_dir):
    paths = []
    root_dir = os.path.abspath(root_dir)  # Ensure the root directory is an absolute path
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            # Remove the root directory part from the full path
            relative_path = os.path.relpath(full_path, root_dir)
            # Filter paths to include only those containing the filter word 
            paths = [path for path in paths if filter_word in path]
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
            result = first_title.get('properties', {}).get('text', {}).get('expr', {}).get('Literal', {}).get('Value', None)        
            return data.get('visual', {}).get('visualType', None), result
    except (FileNotFoundError, json.JSONDecodeError):
        return None
 
def count_visual_links(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Navigate to the visualLink property
        visual_links = data.get('visual', {}).get('visualContainerObjects', {}).get('visualLink', [])
        
        # Count the elements in the visualLink property
        visual_link_count = len(visual_links)
        
        return visual_link_count 
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    
# Save the DataFrame to a CSV file or print it
def save_dataframe(df, file_name):
    df.to_csv(file_name, index=False)



# Example usage
paths = get_paths(root_directory)
df = create_dataframe_from_paths(paths)

# Add a new column for display_name
df['page_name'] = None
df['visual_name'] = None
df['visual_type'] = None
df['visual_link_count'] = None

# Populate the display_name column
for index, row in df.iterrows():
    if row.get('Level_1') == 'bookmarks':
        json_path = os.path.join(root_directory, *row.dropna())
        display_name = get_display_name_from_json(json_path)
        if display_name is not None:
            df.at[index, 'page_name'] = display_name
            
    if row.get('Level_3') == 'page.json':
        json_path = os.path.join(root_directory, *row.dropna())
        display_name = get_display_name_from_json(json_path)
        if display_name is not None:
            df.loc[df['Level_2'] == row['Level_2'], 'page_name'] = display_name
            
    if row.get('Level_3') == 'visuals':
        json_path = os.path.join(root_directory, *row.dropna())
        visual_type, visual_name = get_visual_type_from_json(json_path)
        visual_link_count = count_visual_links(json_path)
        if visual_type is not None:
            df.at[index, 'visual_type'] = visual_type
            df.at[index, 'visual_name'] = visual_name
        df.at[index, 'visual_link_count'] = visual_link_count


#Save file
save_dataframe(df, os.path.join(save_location, file_name))