import os
from google import genai
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(abs_path_working_dir, directory))
        validate_directory = os.path.commonpath([abs_path_working_dir, target_directory]) == abs_path_working_dir

        if not validate_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.exists(target_directory):
            return f'Error: "{directory}" does not exist.'
        
        # if directory == ".":
        #     print(f"Result for current directory:")
        # else:
        #     print(f"Result for '{directory}' directory:")

        file_info =[]
        for items in os.listdir(target_directory):
            file_info.append(f"- {items}, file_size={os.path.getsize(os.path.join(target_directory, items))} bytes, is_dir={os.path.isdir(os.path.join(target_directory, items))}")
            #print(f"- {items}: file_size={os.path.getsize(items)} bytes, is_dir={os.path.isdir(items)}")

        return "\n".join(file_info)
    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)