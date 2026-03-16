"""Smoke tests for the MCP server and tool registration."""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from mcp.server import Server
from src.macro_kiwi.server import app, TOOLS, list_tools, call_tool


@pytest.mark.asyncio
async def test_server_initialization():
    """Test that the server can be initialized."""
    # The app is already created in server.py
    assert isinstance(app, Server)
    assert app.name == "macro-kiwi"


@pytest.mark.asyncio
async def test_list_tools():
    """Test that list_tools returns the expected tools."""
    tools = await list_tools()
    tool_names = [tool.name for tool in tools]
    expected_tools = [
        "generate_dalle_image",
        "edit_image_with_gemini",
        "chat_with_openai",
        "analyze_image_with_vision",
    ]
    for expected in expected_tools:
        assert expected in tool_names


@pytest.mark.asyncio
async def test_call_tool_generate_dalle_image():
    """Test calling generate_dalle_image with mocked API."""
    with patch('src.macro_kiwi.tools.dalle.generate_dalle_image', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "✅ Image generated successfully!"
        
        result = await call_tool(
            "generate_dalle_image",
            {"prompt": "A test image", "quality": "standard", "style": "natural"}
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "✅ Image generated successfully!" in result[0].text
        mock_generate.assert_called_once_with(
            prompt="A test image",
            quality="standard",
            style="natural"
        )


@pytest.mark.asyncio
async def test_call_tool_edit_image_with_gemini():
    """Test calling edit_image_with_gemini with mocked API."""
    with patch('src.macro_kiwi.tools.gemini_edit.edit_image_with_gemini', new_callable=AsyncMock) as mock_edit:
        mock_edit.return_value = "✅ Image edited successfully!"
        
        result = await call_tool(
            "edit_image_with_gemini",
            {
                "image_path": "test.jpg",
                "edit_prompt": "Remove background",
                "output_path": "output.jpg"
            }
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "✅ Image edited successfully!" in result[0].text
        mock_edit.assert_called_once_with(
            image_path="test.jpg",
            edit_prompt="Remove background",
            output_path="output.jpg"
        )


@pytest.mark.asyncio
async def test_call_tool_chat_with_openai():
    """Test calling chat_with_openai with mocked API."""
    with patch('src.macro_kiwi.tools.openai_chat.chat_with_openai', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "**OpenAI Response**\nTest response"
        
        result = await call_tool(
            "chat_with_openai",
            {
                "prompt": "Hello",
                "model": "gpt-4o",
                "max_tokens": 100,
                "temperature": 0.5
            }
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "**OpenAI Response**" in result[0].text
        mock_chat.assert_called_once_with(
            prompt="Hello",
            model="gpt-4o",
            max_tokens=100,
            temperature=0.5
        )


@pytest.mark.asyncio
async def test_call_tool_analyze_image_with_vision():
    """Test calling analyze_image_with_vision with mocked API."""
    with patch('src.macro_kiwi.tools.openai_vision.analyze_image_with_vision', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = "**GPT-4V Image Analysis:**\nTest analysis"
        
        result = await call_tool(
            "analyze_image_with_vision",
            {
                "image_path": "test.jpg",
                "question": "What's in this image?",
                "detail": "auto"
            }
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "**GPT-4V Image Analysis:**" in result[0].text
        mock_analyze.assert_called_once_with(
            image_path="test.jpg",
            question="What's in this image?",
            detail="auto"
        )


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """Test calling an unknown tool raises ValueError."""
    with pytest.raises(ValueError, match="Unknown tool"):
        await call_tool("unknown_tool", {})


def test_tools_schema():
    """Verify each tool has required schema properties."""
    for tool in TOOLS:
        assert tool.name
        assert tool.description
        assert "type" in tool.inputSchema
        assert tool.inputSchema["type"] == "object"
        if "properties" in tool.inputSchema:
            # Check required fields are present
            if "required" in tool.inputSchema:
                for req in tool.inputSchema["required"]:
                    assert req in tool.inputSchema["properties"]
"""Smoke tests for the MCP server and tool registration."""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from mcp.server import Server
from src.macro_kiwi.server import app, TOOLS, list_tools, call_tool


@pytest.mark.asyncio
async def test_server_initialization():
    """Test that the server can be initialized."""
    # The app is already created in server.py
    assert isinstance(app, Server)
    assert app.name == "macro-kiwi"


@pytest.mark.asyncio
async def test_list_tools():
    """Test that list_tools returns the expected tools."""
    tools = await list_tools()
    tool_names = [tool.name for tool in tools]
    expected_tools = [
        "generate_dalle_image",
        "edit_image_with_gemini",
        "chat_with_openai",
        "analyze_image_with_vision",
    ]
    for expected in expected_tools:
        assert expected in tool_names


@pytest.mark.asyncio
async def test_call_tool_generate_dalle_image():
    """Test calling generate_dalle_image with mocked API."""
    with patch('src.macro_kiwi.tools.dalle.generate_dalle_image', new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "✅ Image generated successfully!"
        
        result = await call_tool(
            "generate_dalle_image",
            {"prompt": "A test image", "quality": "standard", "style": "natural"}
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "✅ Image generated successfully!" in result[0].text
        mock_generate.assert_called_once_with(
            prompt="A test image",
            quality="standard",
            style="natural"
        )


@pytest.mark.asyncio
async def test_call_tool_edit_image_with_gemini():
    """Test calling edit_image_with_gemini with mocked API."""
    with patch('src.macro_kiwi.tools.gemini_edit.edit_image_with_gemini', new_callable=AsyncMock) as mock_edit:
        mock_edit.return_value = "✅ Image edited successfully!"
        
        result = await call_tool(
            "edit_image_with_gemini",
            {
                "image_path": "test.jpg",
                "edit_prompt": "Remove background",
                "output_path": "output.jpg"
            }
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "✅ Image edited successfully!" in result[0].text
        mock_edit.assert_called_once_with(
            image_path="test.jpg",
            edit_prompt="Remove background",
            output_path="output.jpg"
        )


@pytest.mark.asyncio
async def test_call_tool_chat_with_openai():
    """Test calling chat_with_openai with mocked API."""
    with patch('src.macro_kiwi.tools.openai_chat.chat_with_openai', new_callable=AsyncMock) as mock_chat:
        mock_chat.return_value = "**OpenAI Response**\nTest response"
        
        result = await call_tool(
            "chat_with_openai",
            {
                "prompt": "Hello",
                "model": "gpt-4o",
                "max_tokens": 100,
                "temperature": 0.5
            }
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "**OpenAI Response**" in result[0].text
        mock_chat.assert_called_once_with(
            prompt="Hello",
            model="gpt-4o",
            max_tokens=100,
            temperature=0.5
        )


@pytest.mark.asyncio
async def test_call_tool_analyze_image_with_vision():
    """Test calling analyze_image_with_vision with mocked API."""
    with patch('src.macro_kiwi.tools.openai_vision.analyze_image_with_vision', new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = "**GPT-4V Image Analysis:**\nTest analysis"
        
        result = await call_tool(
            "analyze_image_with_vision",
            {
                "image_path": "test.jpg",
                "question": "What's in this image?",
                "detail": "auto"
            }
        )
        
        assert len(result) == 1
        assert result[0].type == "text"
        assert "**GPT-4V Image Analysis:**" in result[0].text
        mock_analyze.assert_called_once_with(
            image_path="test.jpg",
            question="What's in this image?",
            detail="auto"
        )


@pytest.mark.asyncio
async def test_call_tool_unknown():
    """Test calling an unknown tool raises ValueError."""
    with pytest.raises(ValueError, match="Unknown tool"):
        await call_tool("unknown_tool", {})


def test_tools_schema():
    """Verify each tool has required schema properties."""
    for tool in TOOLS:
        assert tool.name
        assert tool.description
        assert "type" in tool.inputSchema
        assert tool.inputSchema["type"] == "object"
        if "properties" in tool.inputSchema:
            # Check required fields are present
            if "required" in tool.inputSchema:
                for req in tool.inputSchema["required"]:
                    assert req in tool.inputSchema["properties"]
