from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class LanguageModelInterface(ABC):
    @abstractmethod
    def generate_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, str]]] = None,
        reasoning_effort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a completion from the language model.

        Args:
            model (str): The name of the language model to use.
            messages (List[Dict[str, str]]): A list of messages for the conversation.
            tools (Optional[List[Dict[str, str]]]): Optional tools to assist in generating the response.
            reasoning_effort (Optional[str]): Optional reasoning effort level.

        Returns:
            Dict[str, Any]: The generated completion and related metadata.
        """
        pass