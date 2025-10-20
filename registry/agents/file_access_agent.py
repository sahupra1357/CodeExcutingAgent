import logging
import os

from object_orinted_agents.utils.logger import get_logger
from object_orinted_agents.core.tool_manager import ToolManager
from object_orinted_agents.core.base_agent import BaseAgent
from object_orinted_agents.services.open_ai_language_model import OpenAILanguageModel

from registry.tools.file_access_tool import FileAccessTool

import dotenv
dotenv.load_dotenv()

myapp_logger = get_logger(__name__, logging.INFO)

language_model_ai_interface = OpenAILanguageModel(api_key=os.getenv("OPENAI_API_KEY"), logger=myapp_logger)

class FileAccessAgent(BaseAgent):
    def __init__(
        self,
        developer_prompt: str = """You are a helpful data science assistant.
        The user will provide the name of the csv file that contains relationals data. The file in in directory ./data.
        Instructions:
        1. When user provides the CSV file name, use the 'safe_read_file' tool to read and display first 15 lines of the file.
        2. If specified file doesn't exists in the provided path, return appropriate error message.
        3. User may request data analysis based on file contents, but you should NOT perform or write ant code for any data analysis. Your only task is to read and return the first 6 lines of the file.
        """,
        model_name: str = "gpt-4o",
        logger=myapp_logger,
        language_model_interface: OpenAILanguageModel = language_model_ai_interface,
    ):
        super().__init__(developer_prompt=developer_prompt, model_name=model_name, logger=logger, language_model_interface=language_model_interface)
        self.setup_tools()
    
    def setup_tools(self) -> None:
        """Setup tools for the agent."""
        self.logger.debug("Setting up tools for FileAccessAgent.")
        self.tool_manager = ToolManager(logger=self.logger, language_model_interface=self.language_model_interface)
        file_access_tool = FileAccessTool(logger=self.logger)
        self.tool_manager.register_tool(file_access_tool)
        self.logger.debug("FileAccessTool has been registered with the ToolManager.")