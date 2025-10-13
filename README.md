# Macro Kiwi 🥝

Personal MCP server for unified access to multiple generative AI services from Claude Code.

## Features

### 🎨 Image Generation
- **DALL-E 3**: High-quality image generation from text descriptions
- Automatically downloads and saves images locally with metadata
- Quality options: standard ($0.04) or HD ($0.08)
- Style options: natural or vivid

### ✂️ Image Editing
- **Nano Banana (Gemini 2.5 Flash Image)**: ⭐ EXTREMELY CAPABLE image editor
- Production-ready model released October 2025
- Excellent for "last mile" polish - final refinements, quick iterations, professional finishing touches
- Uses simple conversational text prompts - no complex masking required!
- Perfect for: background removal/replacement, adding/removing elements, style changes, color adjustments, fixing artifacts, artistic modifications, composition changes
- Handles sophisticated edits naturally - your go-to for making images delivery-ready
- Cost: ~$0.039 per 1024x1024 image

### 💬 Text Completion
- **OpenAI GPT Models**: Access to GPT-5, GPT-5 Pro, GPT-4o, GPT-4o-mini, o1-preview, o1-mini
- ⚠️ **IMPORTANT**: Only use when OpenAI/ChatGPT is explicitly requested
- Continue using Claude Code's built-in capabilities for Claude requests
- GPT-5 (default): Best unified model, combines reasoning + speed
- GPT-5 Pro: High-accuracy for finance/legal/healthcare
- o1 models: Specialized reasoning tasks

### 👁️ Image Analysis
- **GPT-4V (Vision)**: Comprehensive image understanding
- Object identification, text reading (OCR), scene description
- Accessibility descriptions and content analysis

## Installation

```bash
# Clone the project
git clone https://github.com/yourusername/macro-kiwi.git
cd macro-kiwi

# Install dependencies
uv sync

# Copy environment template and add your API keys
cp .env.example .env
# Edit .env with your API keys
```

## API Keys Setup

### OpenAI API Key
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env`: `OPENAI_API_KEY=sk-proj-...`

### Google Gemini API Key
1. Visit https://aistudio.google.com/apikey
2. Create a new API key
3. Add to `.env`: `GOOGLE_GENAI_API_KEY=...`

## Claude Code Configuration

Add to your Claude Code settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "macro-kiwi": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/bryancostanza/Developer/macro-kiwi",
        "run",
        "macro-kiwi"
      ]
    }
  }
}
```

Note: The server automatically loads API keys from the `.env` file in the project directory.

## Available Tools

### `generate_dalle_image`
Generate images with DALL-E 3 and automatically save them locally.

**Parameters:**
- `prompt` (required): Text description of the image
- `quality`: "standard" or "hd" (default: standard)
- `style`: "natural" or "vivid" (default: natural)

**Behavior:**
- Images are automatically downloaded and saved to the current directory
- Filenames include timestamp and sanitized prompt for easy identification
- Metadata file (.txt) saved alongside image with prompts and generation details

**Example:**
```
Generate a DALL-E image: "A serene mountain landscape at sunset with pine trees"
→ Saves: dalle_20251012_163045_A_serene_mountain_landscape.png
→ Plus: dalle_20251012_163045_A_serene_mountain_landscape.txt (metadata)
```

### `edit_image_with_gemini`
⭐ EXTREMELY CAPABLE image editor using Gemini's Nano Banana model.

Excellent for "last mile" refinements - those final touches that make images professional and delivery-ready. Perfect for quick iterations and finishing details that would be tedious with traditional editing tools.

**Parameters:**
- `image_path` (required): Path to image file
- `edit_prompt` (required): Clear description of changes (be specific!)
- `output_path` (required): Where to save edited image

**Capabilities:**
- Background removal/replacement, adding/removing elements
- Style changes, polish & refinement, artistic modifications
- Color adjustments, fixing artifacts, composition changes
- Any image transformation you can describe naturally

**Examples:**
```
Last Mile: "Enhance colors, sharpen details, and remove any artifacts"
Background: "Remove all background and replace with pure white (#FFFFFF)"
Creative: "Add a tiny golden crown on the bird's head with sparkles"
Polish: "Adjust brightness, increase contrast slightly, fix any rough edges"
Artistic: "Make the lighting warmer and add a subtle vignette effect"
```

### `chat_with_openai`
⚠️ **Use only when OpenAI/ChatGPT is specifically requested**

**Parameters:**
- `prompt` (required): Text prompt
- `model`: "gpt-5" (default), "gpt-5-pro", "gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"
- `max_tokens`: Maximum response length
- `temperature`: Creativity level (0-2)

**Model Selection:**
- **gpt-5** (default): Best unified model, combines reasoning + speed (Released Aug 2025)
- **gpt-5-pro**: Highest accuracy for finance/legal/healthcare needs (Released Oct 2025)
- **gpt-4o/gpt-4o-mini**: Previous generation, still solid alternatives
- **o1-preview/o1-mini**: Specialized reasoning models

**Example:**
```
General use: "Explain quantum computing in simple terms"
High-accuracy: Use gpt-5-pro for legal analysis or financial modeling
Reasoning: Use o1-preview for "Solve this complex mathematical proof..."
```

### `analyze_image_with_vision`
Analyze images with GPT-4V.

**Parameters:**
- `image_path` (required): Path to image file
- `question`: Optional specific question
- `detail`: "low", "high", or "auto"

**Example:**
```
Analyze photo.jpg with GPT-4V: "What bird species is shown in this image?"
```

## Usage Examples

### Generate and Edit Workflow
```
1. Generate base image with DALL-E:
   "Generate a blue jay bird illustration on white background"

2. Clean up with Gemini:
   "Remove any gray shadows and ensure pure white background"

3. Analyze result with Vision:
   "Verify the background is completely clean"
```

### Image Analysis Workflow
```
1. Use GPT-4V to understand image:
   "What objects are in this photo?"

2. Generate similar image with DALL-E:
   "Create an illustration similar to [description from analysis]"
```

## Cost Estimates

| Service | Operation | Cost |
|---------|-----------|------|
| DALL-E 3 | Standard quality (1024x1024) | $0.04 |
| DALL-E 3 | HD quality (1024x1024) | $0.08 |
| Gemini Image | Edit 1024x1024 | $0.039 |
| GPT-4o | Text completion | ~$0.005/1K tokens |
| GPT-4V | Image analysis | ~$0.01/image + text tokens |

## Additional APIs to Consider

Based on your use case, you might want to add:

### Image Generation Alternatives
- **Stability AI (Stable Diffusion)**: Open source image generation
- **Replicate**: Access to various specialized models
- **Midjourney API**: High-quality artistic generation (if available)

### Audio/Voice
- **ElevenLabs**: High-quality text-to-speech
- **OpenAI Whisper**: Speech-to-text transcription
- **OpenAI TTS**: Native OpenAI text-to-speech

### Additional Capabilities
- **Anthropic API**: Programmatic Claude access (though Claude Code is preferred)
- **Perplexity API**: Research-augmented responses
- **Google Vision API**: Alternative image analysis
- **HuggingFace**: Access to open source models

Let me know if you'd like any of these added!

## Project Structure

```
macro-kiwi/
├── src/macro_kiwi/
│   ├── __init__.py
│   ├── server.py              # Main MCP server
│   └── tools/
│       ├── __init__.py
│       ├── dalle.py           # DALL-E 3 generation
│       ├── gemini_edit.py     # Nano Banana editing
│       ├── openai_chat.py     # OpenAI text completion
│       └── openai_vision.py   # GPT-4V analysis
├── .env                       # API keys (gitignored)
├── .env.example              # Template
├── pyproject.toml            # Project config
├── uv.lock                   # Dependency lock
└── README.md                 # This file
```

## License

Personal project - use as you wish.
