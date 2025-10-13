"""Personal Gen AI MCP Server - Unified access to multiple generative AI services."""

import logging
import os
from pathlib import Path
from collections.abc import Sequence

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from pydantic import AnyUrl
import anyio

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import tool implementations
from .tools.dalle import generate_dalle_image
from .tools.gemini_edit import edit_image_with_gemini
from .tools.openai_chat import chat_with_openai
from .tools.openai_vision import analyze_image_with_vision

# Initialize server
app = Server("macro-kiwi")

# Available tools
TOOLS = [
    Tool(
        name="generate_dalle_image",
        description=(
            "Generate an image using OpenAI's DALL-E 3 model and automatically save it locally. "
            "Creates high-quality 1024x1024 images from text descriptions. "
            "Images are downloaded and saved to the current directory with timestamp and metadata. "
            "Best for: illustrations, concept art, creative imagery. "
            "Cost: $0.04 per image (standard quality)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Detailed description of the image to generate",
                },
                "quality": {
                    "type": "string",
                    "enum": ["standard", "hd"],
                    "default": "standard",
                    "description": "Image quality (standard=$0.04, hd=$0.08)",
                },
                "style": {
                    "type": "string",
                    "enum": ["vivid", "natural"],
                    "default": "natural",
                    "description": "Image style (vivid=hyper-real, natural=authentic)",
                },
            },
            "required": ["prompt"],
        },
    ),
    Tool(
        name="edit_image_with_gemini",
        description=(
            "Edit images using Google's Gemini 2.5 Flash Image model (Nano Banana). "
            "⭐ EXTREMELY CAPABLE image editor using simple text prompts - no complex masking! "
            "Excellent for 'last mile' refinements: final polish, quick iterations, professional finishing touches. "
            "Perfect for: background removal/replacement, adding/removing elements, style changes, "
            "color adjustments, fixing artifacts, artistic modifications, composition changes. "
            "Handles sophisticated edits naturally through conversational instructions. "
            "Cost: $0.039 per 1024x1024 image."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file to edit",
                },
                "edit_prompt": {
                    "type": "string",
                    "description": (
                        "Text description of what to change. Be specific! "
                        "Example: 'Remove all background and replace with pure white (#FFFFFF)'"
                    ),
                },
                "output_path": {
                    "type": "string",
                    "description": "Path where the edited image should be saved",
                },
            },
            "required": ["image_path", "edit_prompt", "output_path"],
        },
    ),
    Tool(
        name="chat_with_openai",
        description=(
            "⚠️ USE ONLY WHEN EXPLICITLY REQUESTED: OpenAI/ChatGPT text completion. "
            "This tool should ONLY be used when the user specifically asks for OpenAI or ChatGPT. "
            "For all Claude-related requests, continue using Claude Code's built-in capabilities. "
            "Supports GPT-5, GPT-5 Pro, GPT-4o, GPT-4o-mini, o1-preview, o1-mini models."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "The prompt to send to OpenAI",
                },
                "model": {
                    "type": "string",
                    "enum": ["gpt-5", "gpt-5-pro", "gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
                    "default": "gpt-5",
                    "description": "OpenAI model (gpt-5: best unified, gpt-5-pro: high-accuracy reasoning, o1: specialized reasoning)",
                },
                "max_tokens": {
                    "type": "integer",
                    "default": 1000,
                    "description": "Maximum tokens in response",
                },
                "temperature": {
                    "type": "number",
                    "default": 0.7,
                    "minimum": 0,
                    "maximum": 2,
                    "description": "Sampling temperature (0=deterministic, 2=very random)",
                },
            },
            "required": ["prompt"],
        },
    ),
    Tool(
        name="analyze_image_with_vision",
        description=(
            "Analyze an image using OpenAI's GPT-4V (Vision) model. "
            "Describes image content, identifies objects, reads text, provides detailed analysis. "
            "Best for: image understanding, OCR, content moderation, accessibility descriptions."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file to analyze",
                },
                "question": {
                    "type": "string",
                    "description": (
                        "Optional specific question about the image. "
                        "If not provided, will give general description."
                    ),
                },
                "detail": {
                    "type": "string",
                    "enum": ["low", "high", "auto"],
                    "default": "auto",
                    "description": "Analysis detail level (high=more tokens, more detail)",
                },
            },
            "required": ["image_path"],
        },
    ),
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Call a tool with given arguments."""
    try:
        if name == "generate_dalle_image":
            result = await generate_dalle_image(
                prompt=arguments["prompt"],
                quality=arguments.get("quality", "standard"),
                style=arguments.get("style", "natural"),
            )
            return [TextContent(type="text", text=result)]

        elif name == "edit_image_with_gemini":
            result = await edit_image_with_gemini(
                image_path=arguments["image_path"],
                edit_prompt=arguments["edit_prompt"],
                output_path=arguments["output_path"],
            )
            return [TextContent(type="text", text=result)]

        elif name == "chat_with_openai":
            result = await chat_with_openai(
                prompt=arguments["prompt"],
                model=arguments.get("model", "gpt-4o"),
                max_tokens=arguments.get("max_tokens", 1000),
                temperature=arguments.get("temperature", 0.7),
            )
            return [TextContent(type="text", text=result)]

        elif name == "analyze_image_with_vision":
            result = await analyze_image_with_vision(
                image_path=arguments["image_path"],
                question=arguments.get("question"),
                detail=arguments.get("detail", "auto"),
            )
            return [TextContent(type="text", text=result)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error calling tool {name}: {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def run():
    """Entry point for the macro-kiwi command."""
    anyio.run(main)


if __name__ == "__main__":
    run()
