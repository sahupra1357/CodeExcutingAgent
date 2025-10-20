from abc import ABC, abstractmethod
from typing import Any, Dict

class ToolInterface(ABC):
    @abstractmethod
    def get_defination(self) -> Dict[str, Any]:
        """
        Retrun JSON/dict defination of the tool's fuction.
        Example:
            {
                "function": {
                    "name": "<tool_fuction_name>",
                    "description": "<what this fuction does>",
                    "parameters": {<JSON schema>}
                }
            }
        """
        pass

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> Any:
        """
        Execute the tool's function with the given arguments.

        Args:
            arguments (Dict[str, Any]): The arguments required to execute the tool's function.

        Returns:
            Any: The result of the tool's function execution.
        """
        pass

    
