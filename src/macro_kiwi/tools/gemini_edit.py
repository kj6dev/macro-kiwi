"""Gemini 2.5 Flash Image (Nano Banana) image editing tool."""

import logging
import os
from io import BytesIO
from pathlib import Path

from google import genai
from PIL import Image

logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))


async def edit_image_with_gemini(
    image_path: str,
    edit_prompt: str,
    output_path: str,
) -> str:
    """
    Edit an image using Google's Gemini 2.5 Flash Image model (Nano Banana).

    ⭐ EXTREMELY CAPABLE image editor using simple text prompts - no complex masking!
    Handles sophisticated edits naturally through conversational instructions.

    Excellent for "last mile" refinements - those final polish touches that make images
    professional and delivery-ready. Perfect for quick iterations, small adjustments,
    and finishing details that would be tedious with traditional tools.

    Capabilities: background removal/replacement, adding/removing elements, style changes,
    polish and refinement, color adjustments, fixing artifacts, artistic modifications,
    composition changes, and any other image transformations you can describe.

    Args:
        image_path: Path to the image file to edit
        edit_prompt: Text description of what to change (be specific for best results)
        output_path: Path where edited image should be saved

    Returns:
        Status message with edit details
    """
    try:
        logger.info(f"Editing image with Gemini: {image_path}")
        logger.info(f"Edit prompt: {edit_prompt}")

        # Read input image
        input_path = Path(image_path)
        if not input_path.exists():
            return f"❌ Error: Input image not found: {image_path}"

        # Load image with PIL
        image = Image.open(input_path)

        # Generate edited image
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[edit_prompt, image],  # Prompt first, then image
        )

        # Check if image was generated
        if not response.candidates:
            return f"❌ Error: No candidates in response\nPrompt feedback: {response.prompt_feedback}"

        # Extract image from response parts
        edited_image_data = None
        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data is not None:
                edited_image_data = part.inline_data.data
                break

        if not edited_image_data:
            return "❌ Error: No image data in Gemini response"

        # Save edited image
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        edited_image = Image.open(BytesIO(edited_image_data))
        edited_image.save(output_file)

        result = f"✅ Image edited successfully!\n\n"
        result += f"**Input Image:** {image_path}\n"
        result += f"**Output Image:** {output_path}\n"
        result += f"**Edit Prompt:** {edit_prompt}\n"
        result += f"**Model:** Gemini 2.5 Flash Image (Nano Banana)\n"
        result += f"**Cost:** ~$0.039 per 1024x1024 image\n"

        return result

    except Exception as e:
        logger.error(f"Error editing image with Gemini: {e}", exc_info=True)
        return f"❌ Error editing image: {str(e)}"
