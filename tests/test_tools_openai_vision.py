"""Unit tests for OpenAI Vision tool."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.macro_kiwi.tools.openai_vision import analyze_image_with_vision


@pytest.mark.asyncio
async def test_analyze_image_with_vision_success():
    """Test successful image analysis."""
    with patch('src.macro_kiwi.tools.openai_vision.client.chat.completions.create', new_callable=AsyncMock) as mock_create:
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "This is a test image analysis."
        mock_response.choices = [mock_choice]
        mock_response.usage = MagicMock(total_tokens=100, prompt_tokens=30, completion_tokens=70)
        mock_create.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.openai_vision.Path') as mock_path:
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path.return_value = mock_path_instance
            
            with patch('src.macro_kiwi.tools.openai_vision.encode_image') as mock_encode:
                mock_encode.return_value = "base64encoded"
                
                result = await analyze_image_with_vision(
                    image_path="test.jpg",
                    question="What's in this image?",
                    detail="auto"
                )
                
                assert "**GPT-4V Image Analysis:**" in result
                assert "This is a test image analysis." in result


@pytest.mark.asyncio
async def test_analyze_image_with_vision_image_not_found():
    """Test when image doesn't exist."""
    with patch('src.macro_kiwi.tools.openai_vision.Path') as mock_path:
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        result = await analyze_image_with_vision(image_path="nonexistent.jpg")
        
        assert "❌ Error: Image not found" in result


@pytest.mark.asyncio
async def test_analyze_image_with_vision_exception():
    """Test exception handling."""
    with patch('src.macro_kiwi.tools.openai_vision.Path') as mock_path:
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        
        with patch('src.macro_kiwi.tools.openai_vision.encode_image') as mock_encode:
            mock_encode.side_effect = Exception("Encoding error")
            
            result = await analyze_image_with_vision(image_path="test.jpg")
            
            assert "❌ Error analyzing image" in result
"""Unit tests for OpenAI Vision tool."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.macro_kiwi.tools.openai_vision import analyze_image_with_vision


@pytest.mark.asyncio
async def test_analyze_image_with_vision_success():
    """Test successful image analysis."""
    with patch('src.macro_kiwi.tools.openai_vision.client.chat.completions.create', new_callable=AsyncMock) as mock_create:
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "This is a test image analysis."
        mock_response.choices = [mock_choice]
        mock_response.usage = MagicMock(total_tokens=100, prompt_tokens=30, completion_tokens=70)
        mock_create.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.openai_vision.Path') as mock_path:
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path.return_value = mock_path_instance
            
            with patch('src.macro_kiwi.tools.openai_vision.encode_image') as mock_encode:
                mock_encode.return_value = "base64encoded"
                
                result = await analyze_image_with_vision(
                    image_path="test.jpg",
                    question="What's in this image?",
                    detail="auto"
                )
                
                assert "**GPT-4V Image Analysis:**" in result
                assert "This is a test image analysis." in result


@pytest.mark.asyncio
async def test_analyze_image_with_vision_image_not_found():
    """Test when image doesn't exist."""
    with patch('src.macro_kiwi.tools.openai_vision.Path') as mock_path:
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        result = await analyze_image_with_vision(image_path="nonexistent.jpg")
        
        assert "❌ Error: Image not found" in result


@pytest.mark.asyncio
async def test_analyze_image_with_vision_exception():
    """Test exception handling."""
    with patch('src.macro_kiwi.tools.openai_vision.Path') as mock_path:
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        
        with patch('src.macro_kiwi.tools.openai_vision.encode_image') as mock_encode:
            mock_encode.side_effect = Exception("Encoding error")
            
            result = await analyze_image_with_vision(image_path="test.jpg")
            
            assert "❌ Error analyzing image" in result
