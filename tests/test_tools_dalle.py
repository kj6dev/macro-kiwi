"""Unit tests for DALL-E image generation tool."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.macro_kiwi.tools.dalle import generate_dalle_image


@pytest.mark.asyncio
async def test_generate_dalle_image_success():
    """Test successful image generation."""
    with patch('src.macro_kiwi.tools.dalle.client.images.generate', new_callable=AsyncMock) as mock_generate:
        mock_response = MagicMock()
        mock_response.data = [MagicMock(url="https://example.com/image.png", revised_prompt="Revised test prompt")]
        mock_generate.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.dalle.httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            mock_http_response = MagicMock()
            mock_http_response.content = b"fake image data"
            mock_http_response.raise_for_status = MagicMock()
            mock_client.get.return_value = mock_http_response
            
            result = await generate_dalle_image(
                prompt="A beautiful sunset",
                quality="standard",
                style="natural"
            )
            
            assert "✅ Image generated and saved successfully!" in result
            assert "Revised test prompt" in result


@pytest.mark.asyncio
async def test_generate_dalle_image_exception():
    """Test exception handling during image generation."""
    with patch('src.macro_kiwi.tools.dalle.client.images.generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.side_effect = Exception("API error")
        
        result = await generate_dalle_image(prompt="test")
        
        assert "❌ Error generating image" in result
"""Unit tests for DALL-E image generation tool."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.macro_kiwi.tools.dalle import generate_dalle_image


@pytest.mark.asyncio
async def test_generate_dalle_image_success():
    """Test successful image generation."""
    with patch('src.macro_kiwi.tools.dalle.client.images.generate', new_callable=AsyncMock) as mock_generate:
        mock_response = MagicMock()
        mock_response.data = [MagicMock(url="https://example.com/image.png", revised_prompt="Revised test prompt")]
        mock_generate.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.dalle.httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value.__aenter__.return_value = mock_client
            
            mock_http_response = MagicMock()
            mock_http_response.content = b"fake image data"
            mock_http_response.raise_for_status = MagicMock()
            mock_client.get.return_value = mock_http_response
            
            result = await generate_dalle_image(
                prompt="A beautiful sunset",
                quality="standard",
                style="natural"
            )
            
            assert "✅ Image generated and saved successfully!" in result
            assert "Revised test prompt" in result


@pytest.mark.asyncio
async def test_generate_dalle_image_exception():
    """Test exception handling during image generation."""
    with patch('src.macro_kiwi.tools.dalle.client.images.generate', new_callable=AsyncMock) as mock_generate:
        mock_generate.side_effect = Exception("API error")
        
        result = await generate_dalle_image(prompt="test")
        
        assert "❌ Error generating image" in result
