from typing import Any, Dict, List, Optional
import pandas as pd
import subprocess
import os

from object_orinted_agents.utils.logger import get_logger
from object_orinted_agents.core.tool_interface import ToolInterface


class FileAccessTool(ToolInterface):
    def __init__(self, logger=None):
        self.logger = logger or get_logger(self.__class__.__name__)

    def get_defination(self) -> Dict[str, Any]:
        self.logger.debug("Getting tool defination for FileAccessTool.")
        return {
            "type": "function",
            "function": {
                "name": "save_file_access",
                "description": (
                    "Read content of a file in secure mannner "
                    "and tranfer it to Python code interpreter docker container."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Name of the file to be read.",
                        },
                    },
                    "required": ["filename"],
                },
            }
        }

    def execute(self, arguments: Dict[str, Any]) -> str:
        filename = arguments.get("filename")
        self.logger.debug(f"Executing FileAccessTool with arguments: {filename}")

        return self.save_file_access(filename)

    def save_file_access(self, filename: str) -> str:
        """
        Read the content of a file and transfer it to the Python code interpreter docker container.

        Args:
            filename (str): The name of the file to be read.
        Returns:
            str: The content of the file or an error message.
        """
        if not filename.endswith(".csv"):
            error_msg = "Error: the file name is not a csv file"
            self.logger.error(error_msg)
            return error_msg   

        if not os.path.isfile(filename):

            filename = os.path.join("./data", filename)

        self.logger.debug(f"Reading file: {filename}")

        try:
            df = pd.read_csv(filename)
            self.logger.info(f"File {filename} read successfully.")
            copy_output = self.copy_file_to_docker(filename)
            head_str = df.head(15).to_string()             
            return f"File content (first 15 rows):\n{head_str}\n\n{copy_output}"
        except Exception as e:
            error_msg = f"Error reading file {filename}: {e}"
            self.logger.error(error_msg)
            return error_msg    
        except FileNotFoundError:
            error_msg = f"Error: File {filename} not found."
            self.logger.error(error_msg)
            return error_msg
        

    def copy_file_to_docker(self, local_file_name: str, container_name: str = "python_sandbox") -> str:
        container_home_path = "/home/sandboxuser/"
        self.logger.debug(f"Copying file {local_file_name} to Docker container {container_name}:{container_home_path}")
        
        if not os.path.isfile(local_file_name):
            error_msg = f"Error: File {local_file_name} not found."
            self.logger.error(error_msg)
            return FileNotFoundError(error_msg)
        
        check_container_cmd = ["docker", "inspect", "-f", "{{.State.Running}}", container_name]
        result = subprocess.run(check_container_cmd, capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "true":
            error_msg = f"Error: Docker container '{container_name}' is not running."
            self.logger.error(error_msg)
            return RuntimeError(error_msg)
        
        container_path = f"{container_name}:{container_home_path}{os.path.basename(local_file_name)}"
        self.logger.debug(f"Running command: docker cp {local_file_name} {container_path}")
        copy_cmd = ["docker", "cp", local_file_name, container_path]
        result = subprocess.run(copy_cmd, check=True, capture_output=True, text=True)

        verify_cmd = ["docker", "exec", container_name, "test", "-f", f"{container_home_path}{os.path.basename(local_file_name)}"]
        verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
        if verify_result.returncode != 0:
            error_msg = f"Error: File {local_file_name} was not copied successfully to the container."
            self.logger.error(error_msg)
            return RuntimeError(error_msg)
        
        success_msg = f"File {local_file_name} copied successfully to the container."
        self.logger.info(success_msg)
        return success_msg
        

