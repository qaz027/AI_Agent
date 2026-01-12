import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_path_working_dir, file_path))
        validate_file = os.path.commonpath([abs_path_working_dir, target_file_path]) == abs_path_working_dir

        if not validate_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # file_path points to a directory
        if os.path.exists(target_file_path) and os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure the directory exists
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, 'w') as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
    
# need to update    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file to which content will be written within the specified directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that should be copied and written to the specified file"
            ),
        },
        required=["file_path","content"],
    ),
)