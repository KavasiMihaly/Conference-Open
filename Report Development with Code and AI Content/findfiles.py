import os
import csv
from datetime import datetime

# Create a script to find and list the files in a directory that have specific words in it.
def find_files_with_words(directory, words):
    # Add a counter to count the number of files that have been checked
    file_count = 0
    matching_file_count = 0
    matching_files = []
    print()
    print("Checking files in directory: {}".format(directory))
    print("Words to search for: {}".format(words))
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_count += 1
            # Print the number of files checked and the number of matching files by overwriting the previous line
            print("\rNumber of files checked: {} | Number of matching files: {}".format(file_count, matching_file_count), end='')
            try:
                with open(file_path, 'r') as f:
                    file_content = f.read()
                    if all(word in file_content for word in words):
                        matching_files.append(file_path)
                        matching_file_count += 1
            
            except:
                continue
    
    return matching_files

def read_search_parameters_from_csv(file_path):
    search_parameters = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    directory = row[0]
                    words = [word.strip() for word in row[1].split(',')]
                    search_parameters.append((directory, words))
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    return search_parameters

def save_matching_files_to_csv(files, words, directory, current_date):
    #change the . to _ in the words to avoid issues with file extensions
    save_file = "matching_files_{}_{}.csv".format("_".join(words).replace(" ", "_").replace(".", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_"), current_date)
    save_file = os.path.join(directory, save_file)
    
    with open(save_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Matching Files for words: {}".format(", ".join(words))])
        for f in files:
            writer.writerow([f])
    
    return save_file

# Example usage --------------------------------------------------------------
# Define the directory to save the results
save_directory = r"C:\Users\kavas\OneDrive\Documents\GitHub\Python-Scripts\Save Files"
# Define the directories to search in and the words to search for
input_file_location = r"C:\Users\kavas\OneDrive\Documents\GitHub\Python-Scripts\search_words.csv"
#Extract the current date
current_date = datetime.now().strftime("%Y%m%d")
# Read the search parameters from the CSV file
search_parameters = read_search_parameters_from_csv(input_file_location)
# Search for the words in the specified directories
print("Searching for the following words in the specified directories:" , search_parameters)
for directory, words in search_parameters:
    if not os.path.exists(directory):
        print(f"Error: The directory {directory} does not exist.")
        continue
    # Find the files that contain the specified words
    files = find_files_with_words(directory, words)
    # Save the matching files to a CSV file
    save_file = save_matching_files_to_csv(files, words, save_directory, current_date)
    print()
    print(f"Results saved to {save_file}")

