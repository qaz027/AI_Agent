
import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_path_working_dir, file_path))
        validate_file = os.path.commonpath([abs_path_working_dir, target_file_path]) == abs_path_working_dir

        if not validate_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_file_path):
            return f'Error: "{file_path}" does not exist.'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        #MAX_CHARS = 10000
        with open(target_file_path, 'r') as file:
            content = file.read(MAX_CHARS)

            # After reading the first MAX_CHARS...
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'        
        return content
    
    except Exception as e:
        return f"Error reading file: {e}"
    
# need to update    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to file to read, relative to working directory",
            ),
        },
        required=["file_path"],
    ),
)