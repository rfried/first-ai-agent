import os

MAX_CHARS = 10000  # Maximum characters to read from the file

def get_file_content(working_directory, file_path):
    """
    Get the content of a file.
    
    Args:
        working_directory (str): The base directory to search for files.
        file_path (str): The path to the file relative to the working directory.
        
    Returns:
        str: The content of the file or an error message if the file does not exist.
    """
    
    
    absolute_working_dir = os.path.abspath(working_directory)    
    full_path = os.path.join(absolute_working_dir, file_path)
    absolute_file_path = os.path.abspath(full_path)

    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(absolute_file_path, 'r') as file:
            content = file.read(MAX_CHARS)
        return content
    except Exception as e:
        return f"Error: reading file {e}"