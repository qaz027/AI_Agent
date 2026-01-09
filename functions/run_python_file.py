import os

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path_working_dir, directory))
        target_file_path = os.path.normpath(os.path.join(abs_path_working_dir, file_path))
        validate_file = os.path.commonpath([abs_path_working_dir, target_file_path]) == abs_path_working_dir
        if os.path.commonpath([abs_path_working_dir, target_dir]) != abs_path_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

    except Exception as e:
        return f"Error: executing Python file: {e}"
