"""OpenAI client wrapper with singleton pattern."""

from openai import OpenAI
from typing import Optional, List, Dict, Any
import tiktoken
from config.settings import settings
from src.utils.logger import get_logger
from src.utils.exceptions import LLMServiceError

logger = get_logger(__name__)


class OpenAIClient:
    """Singleton OpenAI client wrapper."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize OpenAI client."""
        if not self._initialized:
            self.api_client = OpenAI(api_key=settings.openai_api_key)
            self.primary_model = settings.openai_model_primary
            self.secondary_model = settings.openai_model_secondary
            self.max_tokens = settings.openai_max_tokens
            self._initialized = True
            logger.info(f"OpenAI client initialized with models: {self.primary_model}, {self.secondary_model}")

    def count_tokens(self, text: str, model: str = None) -> int:
        """Count tokens in text."""
        try:
            model = model or self.primary_model
            # Use appropriate encoding for the model
            if "gpt-4" in model:
                encoding = tiktoken.encoding_for_model("gpt-4")
            else:
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

            return len(encoding.encode(text))
        except Exception as e:
            logger.warning(f"Error counting tokens: {e}, using estimate")
            return len(text) // 4  # Rough estimate

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion."""
        try:
            model = model or self.primary_model
            max_tokens = max_tokens or self.max_tokens

            logger.debug(f"Calling OpenAI API with model {model}")

            response = self.api_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            logger.info(f"OpenAI API call successful. Tokens used: {tokens_used}")
            return content

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise LLMServiceError(f"OpenAI API error: {str(e)}")

    def simple_completion(
        self, prompt: str, model: Optional[str] = None, temperature: float = 0.7
    ) -> str:
        """Simple completion with a single prompt."""
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages, model, temperature)

    def structured_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """Completion with system and user messages."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.chat_completion(messages, model, temperature)

    def generate_embeddings(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Generate embeddings for text."""
        try:
            response = self.api_client.embeddings.create(input=text, model=model)
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")
            return embedding

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise LLMServiceError(f"Embedding generation error: {e}")

# Global client instance
client = OpenAIClient()

