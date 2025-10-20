import subprocess
from typing import Any, Dict, Tuple

from object_orinted_agents.core.tool_interface import ToolInterface
from object_orinted_agents.utils.logger import get_logger

class PythonCodeInterpreterTool(ToolInterface):
    def __init__(self, logger=None):
        self.logger = logger or get_logger(self.__class__.__name__)
    def get_defination(self):
        return {
            "type": "function",
            "function": {
                "name": "python_code_interpreter",
                "description": (
                    "Executes Python code in a secure, isolated environment. "
                    "This tool is useful for performing calculations, data analysis, "
                    "and other tasks that require Python code execution."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "python_code": {
                            "type": "string",
                            "description": "The Python code to be executed."
                        },
                    },
                    "required": ["python_code"]
                }
            }
        }  
    
    def execute(self, arguments: Dict[str, Any]) -> Any:
        python_code = arguments.get("python_code")
        python_code_stripped = python_code.strip('"""')
        
        self.logger.info(f"Executing Python code: {python_code_stripped}")
        output, errors = self._run_code_in_docker(python_code_stripped)
        if errors:
            return f"Error: {errors}"
        return output
    
    @staticmethod
    def _run_code_in_docker(code: str, container_name: str = "python_sandbox") -> Tuple[str, str]:

        cmd = ["docker", "exec", "-i", container_name, "python3", "-c", "import sys; exec(sys.stdin.read())"]

        proces = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = proces.communicate(input=code)
        return output, errors
    

