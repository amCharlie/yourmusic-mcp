# YourMusic.Fun MCP Server

<div class="title-block" style="text-align: center;" align="center">

# 🎵 YourMusic.Fun MCP Server

**AI-Powered Music Generation with Model Context Protocol**

</div>

<p align="center">
  Official YourMusic.Fun Model Context Protocol (MCP) server that enables seamless interaction with our advanced AI music generation platform. This server allows MCP clients like <a href="https://www.anthropic.com/claude">Claude Desktop</a>, <a href="https://github.com/openai/openai-agents-python">OpenAI Agents</a> and others to generate and play AI-generated music through natural language commands.
</p>

## ✨ Features

- **🎼 AI Music Generation**: Generate songs based on text prompts using YourMusic.Fun's state-of-the-art AI models
- **🎵 Dual Generation Modes**: Support for both inspiration mode and custom mode
- **🔊 Audio Playback**: Play generated audio files directly in your MCP client
- **📁 Flexible Output**: Save generated music to custom directories or default to desktop
- **🤖 Multiple Models**: Support for different AI models including chirp-4.5+ and chirp-4.5
- **🎹 Instrumental Options**: Generate instrumental-only music or full songs with vocals
- **⚡ Async Processing**: Efficient asynchronous handling of long-running music generation tasks

## 🚀 Quickstart with Claude Desktop

1. **Get Your API Key**: Obtain your API key from [YourMusic.Fun Platform](https://app.yourmusic.fun)
2. **Install uv**: Install the Python package manager with `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **Configure Claude**: Go to Claude > Settings > Developer > Edit Config > claude_desktop_config.json and add:

```json
{
    "mcpServers": {
        "YourMusic.Fun": {
            "command": "uvx",
            "args": [
                "yourmusic-fun-mcp"
            ],
            "env": {
                "YOURMUSIC_API_KEY": "<insert-your-api-key-here>",
                "YOURMUSIC_API_URL": "https://app.yourmusic.fun",
                "TIME_OUT_SECONDS": "600",
                "YOURMUSIC_MCP_BASE_PATH": "~/Desktop"
            }
        }
    }
}
```

4. **Restart Claude**: Restart the Claude app and you'll see 3 MCP tools available, indicating successful loading

## ⚙️ Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `YOURMUSIC_API_KEY` | Your YourMusic.Fun API key | - | ✅ Yes |
| `YOURMUSIC_API_URL` | YourMusic.Fun API base URL | `https://app.yourmusic.fun` | ❌ No |
| `TIME_OUT_SECONDS` | Timeout for music generation in seconds | `600` (10 min) | ❌ No |
| `YOURMUSIC_MCP_BASE_PATH` | Base path for file operations | `~/Desktop` | ❌ No |

## 🛠️ Available Tools

### 1. 🎼 Generate Prompt Song (灵感模式)
Generate AI music based on simple text descriptions. AI automatically creates title, lyrics, and style.

**Parameters:**
- `prompt` (str): Simple description of the music theme (1-1200 characters)
- `instrumental` (bool, optional): Whether to generate instrumental music only (default: false)
- `model_type` (str, optional): AI model to use (default: 'chirp-v3-5')
- `output_directory` (str, optional): Directory to save the generated music (default: desktop)

**Example Prompts:**
```
"帮我生成一首关于和平早晨的歌"
"想要一首表达思念的歌曲"
"创作一首关于友谊的音乐"
```

**Output Files:** `标题1.mp3`, `标题2.mp3` (AI-generated titles)

### 2. 🎵 Generate Custom Song (自定义模式)
Generate AI music with specific lyrics, title, and style parameters that you provide.

**Parameters:**
- `title` (str): Song title (required)
- `lyric` (str): Complete lyrics content (required)
- `model_type` (str, optional): AI model to use (default: 'chirp-v4')
- `tags` (str, optional): Music style tags (e.g., 'pop', 'rock', 'folk')
- `instrumental` (bool, optional): Whether to generate instrumental music only (default: false)
- `vocal_gender` (str, optional): Vocal gender - 'm' for male, 'f' for female (default: 'm')
- `weirdness_constraint` (float, optional): Weirdness constraint 0.0-1.0 (default: 0.6)
- `style_weight` (float, optional): Style weight 0.0-1.0 (default: 0.7)
- `output_directory` (str, optional): Directory to save the generated music (default: desktop)

**Example Usage:**
```
请帮我生成一首歌
歌名：蝉蜕的夏天
歌词：[完整歌词内容]
使用男声，风格使用民谣
```

**Output Files:** `标题1.mp3`, `标题2.mp3` (using your specified title)

### 3. 🔊 Play Audio
Play an audio file directly in your MCP client with high-quality audio support.

**Parameters:**
- `input_file_path` (str): Path to the audio file to play

**Supported Formats:** WAV, MP3, M4A, AAC, OGG, FLAC, MP4, AVI, MOV, WMV

## 💡 Example Usage

⚠️ **Note**: YourMusic.Fun credits are required to use the music generation tools.

### Try asking Claude:

#### **灵感模式 (Inspiration Mode):**
- "请帮我生成一首关于和平早晨的歌"
- "想要一首表达思念的歌曲"
- "创作一首关于友谊的音乐"

#### **自定义模式 (Custom Mode):**
- "请帮我生成一首歌，歌名：蝉蜕的夏天，歌词：[完整歌词]，使用男声，风格使用民谣"
- "创作一首歌，标题：春天的约定，歌词：[完整歌词]，女声，流行风格"

#### **音频播放:**
- "播放我桌面上的歌曲文件"
- "播放刚生成的音乐"

## 📦 Installation

### Using uv (Recommended)
```bash
uv add yourmusic-fun-mcp
```

### Using pip
```bash
pip install yourmusic-fun-mcp
```

### From Source
```bash
git clone https://github.com/yourmusic-fun/yourmusic-fun-mcp.git
cd yourmusic-fun-mcp
pip install -e .
```

### Quick Install Script
```bash
chmod +x install.sh
./install.sh
```

## 🔌 API Integration

This MCP server integrates with YourMusic.Fun's RESTful API:

- **`POST /generate/prompt`**: Create music generation task (inspiration mode)
- **`POST /generate/custom`**: Create custom music generation task
- **`POST /generate/status`**: Query task status and progress

The server handles the complete workflow:
1. Submit generation request
2. Poll for completion status
3. Download generated audio files
4. Save to specified directory with intelligent naming

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `YOURMUSIC_API_KEY` is set correctly
2. **Timeout Errors**: Increase `TIME_OUT_SECONDS` if music generation takes longer
3. **File Permission Errors**: Check that the output directory is writable
4. **Audio Playback Issues**: Install required audio libraries: `pip install sounddevice soundfile`

### Logs

When running with Claude Desktop, logs can be found at:

- **Windows**: `%APPDATA%\Claude\logs\mcp-server-YourMusic.Fun.log`
- **macOS**: `~/Library/Logs/Claude/mcp-server-YourMusic.Fun.log`

## 🧪 Development

### Running Tests
```bash
pytest tests/
```

### Local Development
```bash
python -m yourmusic_fun_mcp.api
```

### Code Structure
```
yourmusic_fun_mcp/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
└── api.py               # Core MCP server implementation
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by the YourMusic.Fun Team**

*Transform your ideas into music with AI*

</div>
