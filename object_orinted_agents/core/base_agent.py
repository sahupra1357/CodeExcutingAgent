from abc import ABC, abstractmethod
from typing import Optional
from object_orinted_agents.core.agent_signeture import AgentSignature
from object_orinted_agents.core.chat_message import ChatMessages
from object_orinted_agents.services.language_model_interface import LanguageModelInterface  
from object_orinted_agents.core.tool_manager import ToolManager
from object_orinted_agents.utils.logger import get_logger


class BaseAgent(ABC):
    def __init__(self,
                 developer_prompt: str,
                 model_name: str,
                 logger=None,
                 language_model_interface: LanguageModelInterface = None,
                 reasoning_effort: Optional[str] = None
        ):
        self.developer_prompt = developer_prompt
        self.model_name = model_name
        self.messages = ChatMessages(developer_prompt)
        self.tool_manager : Optional[ToolManager] = None
        self.logger = logger or get_logger(self.__class__.__name__)
        self.language_model_interface = language_model_interface
        self.reasoning_effort = reasoning_effort

    @abstractmethod
    def setup_tools(self) -> None:
        """Abstract method to setup tools for the agent."""
        pass

    def add_context(self, content: str) -> None:
        """Add context to the agent's message history."""
        self.messages.add_system_message(content)
        self.logger.debug(f"Added context to messages: {content}")

    def add_messages(self, content: str) -> None:
        """Add a message to the agent's message history."""
        self.messages.add_user_message(content)
        self.logger.debug(f"Added user message: {content}")
        

    def task(self, user_task: str, tool_call_enabled: bool = True, return_tool_response_as_is: bool = False, reasoning_effort: Optional[str] = None) -> str:
        """Process a user task and return the agent's response."""
        self.logger.debug(f"Task method called with: {user_task}...")
        final_reasoning_effort = reasoning_effort if reasoning_effort else self.reasoning_effort

        if self.language_model_interface is None:
            error_msg = "LanguageModelInterface is not set."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.logger.debug(f"Language model interface: {self.language_model_interface}")
        self.logger.debug(f"Task method called with: {user_task[:50]}...")
        self.logger.debug(f"Starting task: {user_task} (tool_call_enabled={tool_call_enabled})")

        # Add user message

        self.add_messages(user_task)

        tools = []
        if tool_call_enabled and self.tool_manager:
            tools = self.tool_manager.get_tool_definitions()
            self.logger.debug(f"Available tools: {tools}")

        params = {
            "model": self.model_name,
            "messages": self.messages.get_messages(),
            "tools": tools,
        }

        if final_reasoning_effort:
            params["reasoning_effort"] = final_reasoning_effort
        
        response = self.language_model_interface.generate_completion(**params)
        tool_calls = response.choices[0].message.tool_calls
        if tool_call_enabled and tool_calls and self.tool_manager:
            self.logger.info(f"Tool call detected in response: {tool_calls}")
            return self.tool_manager.handle_tool_call_sequence(
                response,
                return_tool_response_as_is,
                self.messages,
                self.model_name,
                reasoning_effort=final_reasoning_effort
            )
        
        # No tool call mormal assistance response
        final_message = response.choices[0].message.content
        self.messages.add_assistant_message(final_message)
        self.logger.info(f"Assistant response: {final_message}")
        self.logger.debug("Task completed successfully.")

        return final_message

    def get_agent_signature(self) -> AgentSignature:
        """Get the agent's signature."""
        signature_obj = AgentSignature(
            developer_prompt=self.developer_prompt,
            model_name=self.model_name,
            tool_manager=self.tool_manager,
            reasoning_effort=self.reasoning_effort
        )
        return signature_obj.to_dict()


