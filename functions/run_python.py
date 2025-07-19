import os
import subprocess
from textwrap import dedent
from google.genai import types as genai_types

def run_python_file(working_directory, file_path, args=[]):
    """
    Run a Python file in the specified working directory.
    
    Args:
        working_directory (str): The base directory to run the file in.
        file_path (str): The path to the Python file relative to the working directory.
        
    Returns:
        str: The output of the Python script or an error message if the operation fails.
    """
    
    absolute_working_dir = os.path.abspath(working_directory)
    
    # Strip leading slashes to ensure file_path is treated as relative
    file_path = file_path.lstrip('/')
    
    full_path = os.path.join(absolute_working_dir, file_path)
    absolute_file_path = os.path.abspath(full_path)

    if not absolute_file_path.startswith(absolute_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            args=['python', full_path] + args, 
            cwd=absolute_working_dir, 
            capture_output=True,  # This captures both stdout and stderr
        )
        if len(completed_process.stdout)==0 and len(completed_process.stderr)==0:
            return "No output produced."
        
        result = dedent(f'''
            STDOUT: {completed_process.stdout}
            STDERR: {completed_process.stderr}
        ''').strip()
        
        if completed_process.returncode != 0:
            return f"{result}\nProcess exited with code {completed_process.returncode}"
        else:
            return result
    except subprocess.CalledProcessError as e:
        return f"STDOUT: {e.stdout}\nSTDERR: {e.stderr}\nProcess exited with code {e.returncode}"
    except Exception as e:
        return f"Error: running file {e}"
    
          
schema_run_python_file = genai_types.FunctionDeclaration(
    name="run_python_file",
    description=f"Executes a python file, constrained to the working directory.",
    parameters=genai_types.Schema(
        type=genai_types.Type.OBJECT,
        properties={
            "file_path": genai_types.Schema(
                type=genai_types.Type.STRING,
                description=f"The file path to the python script that will be executed, relative to the working directory.",
            ),
            "args": genai_types.Schema(
                type=genai_types.Type.ARRAY,
                description=f"An array of command line arguments to send to the python script.",
                items=genai_types.Schema(type=genai_types.Type.STRING),
            ),
        },
    ),
)