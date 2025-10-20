import os
from openai import OpenAI
from object_orinted_agents.utils.logger import get_logger

logger = get_logger(__name__)

class OpenAIClientFactory:
    @staticmethod
    def create_client(api_key: str) -> OpenAI:
        """Create and return an OpenAI client instance."""
        resolved_api_key = OpenAIClientFactory._resolve_api_key(api_key)
        return OpenAI(api_key=resolved_api_key)

    @staticmethod
    def _resolve_api_key(api_key: str) -> str:
        if api_key:
            return api_key
        env_api_key = os.getenv("OPENAI_API_KEY")
        if env_api_key:
            return env_api_key
        error_message = " No OpenAI API key provided. Set the OPENAI_API_KEY environment variable or pass the key directly."
        logger.error(error_message)

        raise ValueError(error_message)
