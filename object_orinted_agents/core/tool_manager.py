from object_orinted_agents.services.language_model_interface import LanguageModelInterface
from object_orinted_agents.utils.logger import get_logger
from object_orinted_agents.core.tool_interface import ToolInterface
from object_orinted_agents.core.chat_message import ChatMessages
from typing import Optional
import json

class ToolManager:
    def __init__(self, logger=None, language_model_interface: LanguageModelInterface = None):
        self.tools = {}
        self.logger = logger or get_logger(__name__)
        self.language_model_interface = language_model_interface

    def register_tool(self, tool: ToolInterface) -> None:
        tool_def = tool.get_defination()
        tool_name = tool_def["function"]["name"]
        self.tools[tool_name] = tool
        self.logger.info(f"Registered tool: {tool_name} and its defination: {tool_def}")

    def get_tool_definitions(self):

        definations = []
        for name, tool in self.tools.items():
            tool_def = tool.get_defination()["function"]
            self.logger.debug(f"Tool name: {name}, Defination: {tool_def}")
            definations.append(tool_def)
        return definations
    
    def handle_tool_call_sequence(
            self,
            response,
            return_tool_response_as_is: bool,
            messages: ChatMessages,
            model_name: str,
            reasoning_effort: Optional[str] = None,
        ) -> str:

        first_tool_call = response.choices[0].message.tool_calls[0]
        tool_name = first_tool_call.function.name
        self.logger.info(f"Handing tool call : {tool_name}")

        args = json.loads(first_tool_call.function.arguments)
        self.logger.debug(f"Tool call arguments: {args}")

        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # 1. Invoke tool

        self.logger.info(f"Invoking tool: {tool_name} with args: {args}")
        tool_response = self.tools[tool_name].execute(args)
        self.logger.info(f"Tool '{tool_name}' executed successfully with response: {tool_response}")

        if return_tool_response_as_is:
            self.logger.info(f"Returning tool response as-is without further LLM calls.")
            messages.add_assistant_message(tool_response)
            return tool_response

        self.logger.debug(f"Tool call: {first_tool_call}")
        function_call_result_message = {
            "role" : "tool",
            "content": tool_response,
            "tool_call_id" : first_tool_call.id,
        }

        complete_payload = messages.get_messages()
        complete_payload.append(response.choices[0].message)
        complete_payload.append(function_call_result_message)

        self.logger.debug(f"Calling model again for final answer with payload: {complete_payload}")

        param = {
            "model": model_name,
            "messages": complete_payload,
        }
        if reasoning_effort:
            param["reasoning_effort"] = reasoning_effort

        response_after_tool_call = self.language_model_interface.generate_completion(**param)

        final_message = response_after_tool_call.choices[0].message.content
        self.logger.info(f"Final response after tool call: {final_message}")
        messages.add_assistant_message(final_message)   
    
        return final_message
    
