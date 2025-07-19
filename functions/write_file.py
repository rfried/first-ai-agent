import os
from google.genai import types as genai_types

def write_file(working_directory, file_path, content):
    """
    Write content to a file in the specified working directory.
    
    Args:
        working_directory (str): The base directory to write the file in.
        file_path (str): The path to the file relative to the working directory.
        content (str): The content to write to the file.
        
    Returns:
        str: A success message or an error message if the operation fails.
    """
    
    absolute_working_dir = os.path.abspath(working_directory)
    full_path = os.path.join(absolute_working_dir, file_path)

    
    if not full_path.startswith(absolute_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(os.path.dirname(full_path)):
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

    try:
        with open(full_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing file {e}"
    

schema_write_file = genai_types.FunctionDeclaration(
    name="write_file",
    description=f"Writes text content to a file, constrained to the working directory.",
    parameters=genai_types.Schema(
        type=genai_types.Type.OBJECT,
        properties={
            "file_path": genai_types.Schema(
                type=genai_types.Type.STRING,
                description=f"The file path to write to, relative to the working directory.",
            ),
            "content": genai_types.Schema(
                type=genai_types.Type.STRING,
                description=f"The file content to write into the file path, overriding all previous file content.",
            ),
        },
    ),
)