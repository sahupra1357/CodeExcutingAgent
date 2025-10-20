import logging
import os

from object_orinted_agents.services import language_model_interface
from object_orinted_agents.utils.logger import get_logger
from object_orinted_agents.core.base_agent import BaseAgent
from object_orinted_agents.services.open_ai_language_model import OpenAILanguageModel
from object_orinted_agents.core.tool_manager import ToolManager


from registry.tools.python_code_interpreter_tool import PythonCodeInterpreterTool

myapp_logger = get_logger("My App", logging.INFO)

language_model_ai_interface = OpenAILanguageModel(api_key=os.getenv("OPENAI_API_KEY"), logger=myapp_logger)

class PythonCodeExecAgent(BaseAgent):
    def __init__(
            self,
            developer_prompt: str = """You are a helpful programming assistant.""",
            model_name: str = "o3-mini",
            logger=myapp_logger,
            language_model_interface=language_model_ai_interface,
            reasoning_effort: str = None
    ):
        super().__init__(developer_prompt=developer_prompt, model_name=model_name, logger=logger, language_model_interface=language_model_interface, reasoning_effort=reasoning_effort)
        self.setup_tools()

    def setup_tools(self) -> None:
        """Setup tools for the agent."""
        self.tool_manager = ToolManager(logger=self.logger, language_model_interface=self.language_model_interface)
        self.tool_manager.register_tool(PythonCodeInterpreterTool(logger=self.logger)) 
        self.logger.debug("PythonCodeExecAgent has been registered with the ToolManager.")