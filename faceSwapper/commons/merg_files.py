
import os

def merge_files(directory):
    # Supported file extensions
    supported_extensions = ['.txt', '.html', '.css', '.js', '.py']
    
    # Ensure the input directory exists
    if not os.path.isdir(directory):
        print("The specified directory does not exist.")
        return

    # Extract the directory name
    directory_name = os.path.basename(os.path.normpath(directory))
    
    # Create a new file to store the merged content
    output_file_path = os.path.join(directory, '..', f'merged-{directory_name}.all')
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Write the directory structure at the top
        output_file.write(f'Directory structure of merged files from: {directory}\n')
        output_file.write('=' * 40 + '\n')  # Separator
        
        # Function to print the directory structure in a tree format
        def print_directory_structure(dir_path, prefix=""):
            entries = os.listdir(dir_path)
            for i, entry in enumerate(entries):
                entry_path = os.path.join(dir_path, entry)
                is_last = (i == len(entries) - 1)
                # Determine the prefix for this entry
                connector = '└── ' if is_last else '├── '
                output_file.write(f'{prefix}{connector}{entry}\n')
                if os.path.isdir(entry_path):
                    # If it's a directory, call recursively with updated prefix
                    new_prefix = prefix + ('    ' if is_last else '│   ')
                    print_directory_structure(entry_path, new_prefix)

        # Print the directory structure
        print_directory_structure(directory)

        output_file.write('=' * 40 + '\n\n')  # Separator before contents

        # Walk through the directory again to merge contents
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Check if the file has a supported extension
                if any(file.endswith(ext) for ext in supported_extensions):
                    file_path = os.path.join(root, file)
                    output_file.write(f'Contents of: {file_path}\n')
                    output_file.write('=' * 40 + '\n')  # Separator
                    try:
                        # Open and read the contents of the file
                        with open(file_path, 'r', encoding='utf-8') as input_file:
                            contents = input_file.read()
                            output_file.write(contents + '\n\n')  # Add contents with spacing
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    print(f"Merged file created at: {output_file_path}")

if __name__ == '__main__':
    # Take directory input from user
    input_directory = input("Enter the directory path to crawl: ")
    merge_files(input_directory)
