from object_orinted_agents.services.language_model_interface import LanguageModelInterface
from object_orinted_agents.utils.logger import get_logger
from typing import Any, Dict, List, Optional
from openai import OpenAI
from object_orinted_agents.services.openai_factory import OpenAIClientFactory


class OpenAILanguageModel(LanguageModelInterface):
    def __init__(self, openai_client=None, api_key: Optional[str] = None, logger=None):
        self.logger = logger or get_logger(__name__)
        self.openai_client = openai_client or  OpenAIClientFactory.create_client(api_key)

    def generate_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, str]]] = None,
        reasoning_effort: Optional[str] = None,
    ) -> Dict[str, Any]:
        
        kwargs = {"model": model, 
                  "messages": messages}
        if tools:
            kwargs["tools"] = tools
        if reasoning_effort:
            kwargs["reasoning_effort"] = reasoning_effort
        
        self.logger.debug(f"Generating completion with model: {model}, messages: {messages}, tools: {tools}, reasoning_effort: {reasoning_effort}") 
        
        self.logger.debug("Generating completion with OpenAI model")
        self.logger.debug(f"Requests: {kwargs}")
        try:
            response = self.openai_client.chat.completions.create(**kwargs)
            #response = self.openai_client.responses.create(**kwargs)
            self.logger.debug(f"Received response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error generating completion: {e}")
            raise

