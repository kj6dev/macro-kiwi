"""Gemini image editing tool (Nano Banana models)."""

import logging
import os
from io import BytesIO
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

# Model configurations
# Source: https://ai.google.dev/gemini-api/docs/pricing
MODELS = {
    "flash": {
        "id": "gemini-3.1-flash-image-preview",
        "name": "Gemini 3.1 Flash Image (Nano Banana 2)",
        "max_size": 1024,
        "cost": 0.039,  # $30/M tokens, 1290 tokens/image
    },
    "pro": {
        "id": "gemini-3-pro-image-preview",
        "name": "Gemini 3 Pro Image (Nano Banana Pro)",
        "max_size": 4096,
        "cost": 0.24,  # $0.134 for 1K/2K, $0.24 for 4K
    },
}


async def edit_image_with_gemini(
    image_path: str,
    edit_prompt: str,
    output_path: str,
    model: str = "flash",
) -> str:
    """
    Edit an image using Google's Gemini image models (Nano Banana).

    Two models available:
    - "flash" (default): Gemini 2.5 Flash Image - fast, efficient, 1024px max
    - "pro": Gemini 3 Pro Image - professional-grade, 4096px max, advanced reasoning

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
        model: Model to use ("flash" for speed, "pro" for quality/4K)

    Returns:
        Status message with edit details
    """
    try:
        # Validate model
        if model not in MODELS:
            return f"❌ Invalid model. Choose from: {', '.join(MODELS.keys())}"

        model_config = MODELS[model]
        model_id = model_config["id"]

        logger.info(f"Editing image with {model_id}: {image_path}")
        logger.info(f"Edit prompt: {edit_prompt}")

        # Read input image
        input_path = Path(image_path)
        if not input_path.exists():
            return f"❌ Error: Input image not found: {image_path}"

        # Load image with PIL
        image = Image.open(input_path)

        # Configure generation based on model
        config = None
        if model == "pro":
            # Pro model supports higher resolution and aspect ratio config
            config = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            )

        # Generate edited image
        if config:
            response = client.models.generate_content(
                model=model_id,
                contents=[edit_prompt, image],
                config=config,
            )
        else:
            response = client.models.generate_content(
                model=model_id,
                contents=[edit_prompt, image],
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
        result += f"**Model:** {model_config['name']}\n"
        result += f"**Max Resolution:** {model_config['max_size']}px\n"
        result += f"**Cost:** ~${model_config['cost']:.3f} per image\n"

        return result

    except Exception as e:
        logger.error(f"Error editing image with Gemini: {e}", exc_info=True)
        return f"❌ Error editing image: {str(e)}"
