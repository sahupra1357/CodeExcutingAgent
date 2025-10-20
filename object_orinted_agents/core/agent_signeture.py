from typing import Any, Dict, Optional
from object_orinted_agents.core.tool_manager import ToolManager

class AgentSignature:
    """Class to define the signature of an agent, including its developer prompt, model name, and tools."""
    
    def __init__(
        self,
        developer_prompt: str,
        model_name: str,
        tool_manager: ToolManager,
        reasoning_effort: Optional[str] = None,
    ):
        self.developer_prompt = developer_prompt
        self.model_name = model_name
        self.tool_manager = tool_manager
        self.reasoning_effort = reasoning_effort

    
    def to_dict(self) -> Dict[str, Any]:

        if self.tool_manager:
            tools = self.tool_manager.get_tool_definitions()
            functions = [tool for tool in tools]
        else:
            functions = []

        signeture_dict = {
            "developer_prompt": self.developer_prompt,
            "model_name": self.model_name,
            "tools": functions,
        }

        if self.reasoning_effort:
            signeture_dict["reasoning_effort"] = self.reasoning_effort
        
        return signeture_dict