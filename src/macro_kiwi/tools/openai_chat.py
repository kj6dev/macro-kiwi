"""OpenAI text completion tool.

⚠️ IMPORTANT USAGE WARNING:
This tool should ONLY be used when the user specifically requests OpenAI or ChatGPT.
For all Claude-related requests, continue using Claude Code's built-in capabilities.
"""

import logging
import os

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def chat_with_openai(
    prompt: str,
    model: str = "gpt-5",
    max_tokens: int = 1000,
    temperature: float = 0.7,
) -> str:
    """
    Send a text completion request to OpenAI.

    ⚠️ USE ONLY WHEN EXPLICITLY REQUESTED
    This tool should only be used when the user specifically asks for OpenAI/ChatGPT.
    Continue using Claude Code's built-in capabilities for Claude requests.

    Args:
        prompt: The prompt to send to OpenAI
        model: OpenAI model (gpt-5, gpt-5-pro, gpt-4o, gpt-4o-mini, o1-preview, o1-mini)
        max_tokens: Maximum tokens in response
        temperature: Sampling temperature (0=deterministic, 2=very random)

    Returns:
        The OpenAI response text with metadata
    """
    try:
        logger.info(f"Sending request to OpenAI model: {model}")
        logger.info(f"Prompt: {prompt[:100]}...")

        # Create chat completion
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Extract response
        content = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        usage = response.usage

        result = f"**OpenAI Response ({model}):**\n\n"
        result += f"{content}\n\n"
        result += f"---\n"
        result += f"**Model:** {model}\n"
        result += f"**Finish Reason:** {finish_reason}\n"
        result += f"**Tokens Used:** {usage.total_tokens} "
        result += f"(prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})\n"
        result += f"**Temperature:** {temperature}\n"

        return result

    except Exception as e:
        logger.error(f"Error calling OpenAI: {e}", exc_info=True)
        return f"❌ Error calling OpenAI: {str(e)}"
