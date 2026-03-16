"""Unit tests for Gemini image editing tool."""
import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO
from PIL import Image
from src.macro_kiwi.tools.gemini_edit import edit_image_with_gemini


@pytest.mark.asyncio
async def test_edit_image_with_gemini_success():
    """Test successful image editing."""
    with patch('src.macro_kiwi.tools.gemini_edit.client.models.generate_content') as mock_generate:
        # Mock the response structure
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_part.inline_data.data = b"fake image data"
        mock_candidate.content.parts = [mock_part]
        mock_response.candidates = [mock_candidate]
        mock_generate.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.gemini_edit.Image.open') as mock_open:
            mock_image = MagicMock(spec=Image.Image)
            mock_open.return_value = mock_image
            
            with patch('src.macro_kiwi.tools.gemini_edit.Path') as mock_path:
                mock_path_instance = MagicMock()
                mock_path_instance.exists.return_value = True
                mock_path.return_value = mock_path_instance
                
                result = await edit_image_with_gemini(
                    image_path="input.jpg",
                    edit_prompt="Remove background",
                    output_path="output.jpg"
                )
                
                assert "✅ Image edited successfully!" in result
                assert "Gemini 2.5 Flash Image" in result


@pytest.mark.asyncio
async def test_edit_image_with_gemini_image_not_found():
    """Test when input image doesn't exist."""
    with patch('src.macro_kiwi.tools.gemini_edit.Path') as mock_path:
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        result = await edit_image_with_gemini(
            image_path="nonexistent.jpg",
            edit_prompt="Test",
            output_path="output.jpg"
        )
        
        assert "❌ Error: Input image not found" in result


@pytest.mark.asyncio
async def test_edit_image_with_gemini_no_candidates():
    """Test when response has no candidates."""
    with patch('src.macro_kiwi.tools.gemini_edit.client.models.generate_content') as mock_generate:
        mock_response = MagicMock()
        mock_response.candidates = []
        mock_response.prompt_feedback = "No candidates"
        mock_generate.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.gemini_edit.Path') as mock_path:
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path.return_value = mock_path_instance
            
            with patch('src.macro_kiwi.tools.gemini_edit.Image.open'):
                result = await edit_image_with_gemini(
                    image_path="input.jpg",
                    edit_prompt="Test",
                    output_path="output.jpg"
                )
                
                assert "❌ Error: No candidates in response" in result
"""Unit tests for Gemini image editing tool."""
import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO
from PIL import Image
from src.macro_kiwi.tools.gemini_edit import edit_image_with_gemini


@pytest.mark.asyncio
async def test_edit_image_with_gemini_success():
    """Test successful image editing."""
    with patch('src.macro_kiwi.tools.gemini_edit.client.models.generate_content') as mock_generate:
        # Mock the response structure
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_part = MagicMock()
        mock_part.inline_data = MagicMock()
        mock_part.inline_data.data = b"fake image data"
        mock_candidate.content.parts = [mock_part]
        mock_response.candidates = [mock_candidate]
        mock_generate.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.gemini_edit.Image.open') as mock_open:
            mock_image = MagicMock(spec=Image.Image)
            mock_open.return_value = mock_image
            
            with patch('src.macro_kiwi.tools.gemini_edit.Path') as mock_path:
                mock_path_instance = MagicMock()
                mock_path_instance.exists.return_value = True
                mock_path.return_value = mock_path_instance
                
                result = await edit_image_with_gemini(
                    image_path="input.jpg",
                    edit_prompt="Remove background",
                    output_path="output.jpg"
                )
                
                assert "✅ Image edited successfully!" in result
                assert "Gemini 2.5 Flash Image" in result


@pytest.mark.asyncio
async def test_edit_image_with_gemini_image_not_found():
    """Test when input image doesn't exist."""
    with patch('src.macro_kiwi.tools.gemini_edit.Path') as mock_path:
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        result = await edit_image_with_gemini(
            image_path="nonexistent.jpg",
            edit_prompt="Test",
            output_path="output.jpg"
        )
        
        assert "❌ Error: Input image not found" in result


@pytest.mark.asyncio
async def test_edit_image_with_gemini_no_candidates():
    """Test when response has no candidates."""
    with patch('src.macro_kiwi.tools.gemini_edit.client.models.generate_content') as mock_generate:
        mock_response = MagicMock()
        mock_response.candidates = []
        mock_response.prompt_feedback = "No candidates"
        mock_generate.return_value = mock_response
        
        with patch('src.macro_kiwi.tools.gemini_edit.Path') as mock_path:
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path.return_value = mock_path_instance
            
            with patch('src.macro_kiwi.tools.gemini_edit.Image.open'):
                result = await edit_image_with_gemini(
                    image_path="input.jpg",
                    edit_prompt="Test",
                    output_path="output.jpg"
                )
                
                assert "❌ Error: No candidates in response" in result
