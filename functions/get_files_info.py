import os

def get_files_info(working_directory, directory="."):
    """
    Get information about files in the specified directory.
    
    Args:
        working_directory (str): The base directory to search for files.
        directory (str): The subdirectory to search within the base directory.
        
    Returns:
        list: A list of dictionaries containing file names and their sizes.
    """
    
    full_path = os.path.join(working_directory, directory)

    absolute_working_dir = os.path.abspath(working_directory)
    absolute_dir = os.path.abspath(full_path)

    if not absolute_dir.startswith(absolute_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(absolute_dir):
        return f'Error: "{directory}" is not a directory'
    
    files_info = []
    
    try:
        for filename in os.listdir(full_path):
            file_path = os.path.join(full_path, filename)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            files_info.append(f"- {filename}: file_size={size} bytes, is_dir={is_dir}")
    except FileNotFoundError as e:
        return f"Error: {e}"
        
    return "\n".join(files_info)