"""Unit tests for OpenAI chat tool."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.macro_kiwi.tools.openai_chat import chat_with_openai


@pytest.mark.asyncio
async def test_chat_with_openai_success():
    """Test successful OpenAI chat completion."""
    with patch('src.macro_kiwi.tools.openai_chat.client.chat.completions.create', new_callable=AsyncMock) as mock_create:
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"
        mock_choice.finish_reason = "stop"
        mock_response.choices = [mock_choice]
        mock_response.usage = MagicMock(total_tokens=50, prompt_tokens=10, completion_tokens=40)
        mock_create.return_value = mock_response
        
        result = await chat_with_openai(
            prompt="Hello, how are you?",
            model="gpt-4o",
            max_tokens=100,
            temperature=0.7
        )
        
        assert "**OpenAI Response (gpt-4o):**" in result
        assert "Test response" in result
        assert "Tokens Used: 50" in result


@pytest.mark.asyncio
async def test_chat_with_openai_exception():
    """Test exception handling in OpenAI chat."""
    with patch('src.macro_kiwi.tools.openai_chat.client.chat.completions.create', new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = Exception("API error")
        
        result = await chat_with_openai(prompt="test")
        
        assert "❌ Error calling OpenAI" in result
"""Unit tests for OpenAI chat tool."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.macro_kiwi.tools.openai_chat import chat_with_openai


@pytest.mark.asyncio
async def test_chat_with_openai_success():
    """Test successful OpenAI chat completion."""
    with patch('src.macro_kiwi.tools.openai_chat.client.chat.completions.create', new_callable=AsyncMock) as mock_create:
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "Test response"
        mock_choice.finish_reason = "stop"
        mock_response.choices = [mock_choice]
        mock_response.usage = MagicMock(total_tokens=50, prompt_tokens=10, completion_tokens=40)
        mock_create.return_value = mock_response
        
        result = await chat_with_openai(
            prompt="Hello, how are you?",
            model="gpt-4o",
            max_tokens=100,
            temperature=0.7
        )
        
        assert "**OpenAI Response (gpt-4o):**" in result
        assert "Test response" in result
        assert "Tokens Used: 50" in result


@pytest.mark.asyncio
async def test_chat_with_openai_exception():
    """Test exception handling in OpenAI chat."""
    with patch('src.macro_kiwi.tools.openai_chat.client.chat.completions.create', new_callable=AsyncMock) as mock_create:
        mock_create.side_effect = Exception("API error")
        
        result = await chat_with_openai(prompt="test")
        
        assert "❌ Error calling OpenAI" in result
