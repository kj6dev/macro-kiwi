# macro-kiwi

A personal MCP server that gives Claude Code unified access to image generation, image editing, and other AI services from outside the Anthropic family. One install, one config block, four providers behind a single MCP interface.

> Source: [github.com/kj6dev/macro-kiwi](https://github.com/kj6dev/macro-kiwi). MIT-licensed.

## What it does

Claude Code is already excellent at writing and reading code. What it cannot do natively is generate or edit images, or call other model providers when one of them is the right tool for the job. macro-kiwi fills that gap by exposing four capabilities through MCP:

- **Image generation** via OpenAI DALL-E 3 and `gpt-image-1`. Both quality tiers, both style modes, automatic local download with a sidecar text file capturing the original prompt.
- **Image editing** via Google's Nano Banana (Gemini 2.5 Flash Image). Conversational text prompts replace the masking step, which is how you actually want to do background swaps, element removal, and final polish passes.
- **Image analysis** via GPT-4V. Object identification, OCR, scene description, accessibility text.
- **Text completion** via OpenAI GPT models. This is the escape hatch for cases where you specifically want OpenAI rather than Claude. The MCP description discourages routing Claude-shaped tasks here by accident.

## Install

```bash
git clone git@github.com:kj6dev/macro-kiwi.git
cd macro-kiwi
uv sync
```

API keys are pulled from the process environment at server start. Set `OPENAI_API_KEY` and `GOOGLE_API_KEY` either in a `.env` file or in your MCP client's config block. I keep secrets in `pass` and inject them at server launch.

## Wire it into Claude Code

Add to your `mcp_servers` config:

```json
{
  "macro-kiwi": {
    "command": "uv",
    "args": ["--directory", "/path/to/macro-kiwi", "run", "macro-kiwi"],
    "env": {
      "OPENAI_API_KEY": "...",
      "GOOGLE_API_KEY": "..."
    }
  }
}
```

`synodic-kit` bundles macro-kiwi by default for users of that plugin.

## Why "macro-kiwi"

The name follows a personal naming convention. The functional name would have been "external-providers" or "non-anthropic-mcp," neither of which sparks joy.

## Companion piece

[synodic.co/macro-kiwi](https://synodic.co/macro-kiwi/) has a longer writeup on the design choices and what each provider is good for in practice.
