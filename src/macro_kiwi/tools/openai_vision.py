"""OpenAI Vision (GPT-4V) image analysis tool."""

import base64
import logging
import os
from pathlib import Path

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(image_path: str) -> str:
    """Encode image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def analyze_image_with_vision(
    image_path: str,
    question: str | None = None,
    detail: str = "auto",
) -> str:
    """
    Analyze an image using OpenAI's GPT-4V (Vision) model.

    Can describe image content, identify objects, read text, provide detailed analysis.

    Args:
        image_path: Path to the image file to analyze
        question: Optional specific question about the image
        detail: Analysis detail level (low, high, auto)
                - low: faster, less tokens, basic understanding
                - high: slower, more tokens, fine details
                - auto: model decides based on image

    Returns:
        Analysis results with metadata
    """
    try:
        logger.info(f"Analyzing image with GPT-4V: {image_path}")

        # Validate image exists
        img_path = Path(image_path)
        if not img_path.exists():
            return f"❌ Error: Image not found: {image_path}"

        # Encode image
        base64_image = encode_image(image_path)

        # Determine file type
        mime_type = "image/jpeg"
        if img_path.suffix.lower() == ".png":
            mime_type = "image/png"
        elif img_path.suffix.lower() == ".gif":
            mime_type = "image/gif"
        elif img_path.suffix.lower() == ".webp":
            mime_type = "image/webp"

        # Build prompt
        if question:
            prompt = question
        else:
            prompt = (
                "Please provide a detailed description of this image. "
                "Include information about objects, people, text, colors, composition, "
                "and any other notable features."
            )

        # Create vision request
        response = await client.chat.completions.create(
            model="gpt-4o",  # gpt-4o has vision capabilities
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                                "detail": detail,
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        # Extract response
        content = response.choices[0].message.content
        usage = response.usage

        result = f"**GPT-4V Image Analysis:**\n\n"
        result += f"{content}\n\n"
        result += f"---\n"
        result += f"**Image:** {image_path}\n"
        result += f"**Question:** {question or 'General description'}\n"
        result += f"**Detail Level:** {detail}\n"
        result += f"**Tokens Used:** {usage.total_tokens} "
        result += f"(prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})\n"

        return result

    except Exception as e:
        logger.error(f"Error analyzing image with GPT-4V: {e}", exc_info=True)
        return f"❌ Error analyzing image: {str(e)}"
