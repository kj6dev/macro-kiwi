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
import anyio

# Load secrets from macOS Keychain, fall back to .env
import subprocess
for _svc, _envvar in [("google-genai-api-key", "GOOGLE_GENAI_API_KEY")]:
    _r = subprocess.run(["security", "find-generic-password", "-a", "REDACTED_USER", "-s", _svc, "-w"], capture_output=True, text=True)
    if _r.returncode == 0 and _r.stdout.strip():
        os.environ[_envvar] = _r.stdout.strip()

# Fall back to .env file for any missing values
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import tool implementations
from .tools.gemini_edit import edit_image_with_gemini

# Initialize server
app = Server("macro-kiwi")

# Available tools
TOOLS = [
    Tool(
        name="edit_image_with_gemini",
        description=(
            "Edit images using Google's Gemini image models (Nano Banana). "
            "⭐ EXTREMELY CAPABLE image editor using simple text prompts - no complex masking! "
            "Two models: 'flash' (default, 1024px, fast) or 'pro' (4096px, professional-grade). "
            "Excellent for 'last mile' refinements: final polish, quick iterations, professional finishing touches. "
            "Perfect for: background removal/replacement, adding/removing elements, style changes, "
            "color adjustments, fixing artifacts, artistic modifications, composition changes. "
            "Cost: flash=$0.039, pro=$0.13-0.24 per image."
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
                "model": {
                    "type": "string",
                    "enum": ["flash", "pro"],
                    "default": "flash",
                    "description": "Model: 'flash' (fast, 1024px) or 'pro' (4K, advanced reasoning)",
                },
            },
            "required": ["image_path", "edit_prompt", "output_path"],
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
        if name == "edit_image_with_gemini":
            result = await edit_image_with_gemini(
                image_path=arguments["image_path"],
                edit_prompt=arguments["edit_prompt"],
                output_path=arguments["output_path"],
                model=arguments.get("model", "flash"),
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
