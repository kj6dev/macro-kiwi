"""DALL-E 3 image generation tool."""

import logging
import os
from datetime import datetime
from pathlib import Path

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_dalle_image(
    prompt: str,
    quality: str = "standard",
    style: str = "natural",
    output_path: str | None = None,
    output_dir: str = ".",
) -> str:
    """
    Generate an image using DALL-E 3 and save it locally.

    Args:
        prompt: Text description of the image to generate
        quality: Image quality ("standard" or "hd")
        style: Image style ("vivid" or "natural")
        output_path: Full file path to save image (overrides output_dir and auto-naming)
        output_dir: Directory to save image with auto-generated name (default: current directory)

    Returns:
        Status message with local file path and OpenAI URL
    """
    try:
        logger.info(f"Generating DALL-E image with prompt: {prompt[:100]}...")

        # Generate image
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality=quality,
            style=style,
            n=1,
        )

        # Get image URL and revised prompt
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt

        # Determine save path
        if output_path:
            image_path = Path(output_path)
            image_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            dir_path = Path(output_dir)
            dir_path.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:50] if c.isalnum() or c.isspace())
            safe_prompt = safe_prompt.replace(" ", "_")
            image_filename = f"dalle_{timestamp}_{safe_prompt}.png"
            image_path = dir_path / image_filename

        # Download and save image
        import httpx

        async with httpx.AsyncClient() as http_client:
            image_response = await http_client.get(image_url)
            image_response.raise_for_status()
            image_path.write_bytes(image_response.content)

        # Save metadata
        metadata_path = image_path.with_suffix(".txt")
        metadata = f"Original Prompt:\n{prompt}\n\n"
        metadata += f"Revised Prompt:\n{revised_prompt}\n\n"
        metadata += f"Quality: {quality}\n"
        metadata += f"Style: {style}\n"
        metadata += f"Generated: {datetime.now().isoformat()}\n"
        metadata_path.write_text(metadata)

        result = f"✅ Image generated and saved successfully!\n\n"
        result += f"**Saved to:** {image_path}\n"
        result += f"**Metadata:** {metadata_path}\n\n"
        result += f"**OpenAI URL (temporary):** {image_url}\n\n"
        result += f"**Original Prompt:** {prompt}\n\n"
        result += f"**Revised Prompt (by DALL-E):** {revised_prompt}\n\n"
        result += f"**Quality:** {quality}\n"
        result += f"**Style:** {style}\n"
        result += f"**Cost:** ${'0.08' if quality == 'hd' else '0.04'}\n"

        return result

    except Exception as e:
        logger.error(f"Error generating DALL-E image: {e}", exc_info=True)
        return f"❌ Error generating image: {str(e)}"
