# YourMusic.Fun MCP Server - Project Structure

## Project Overview

This is a Model Context Protocol (MCP) music generation server specifically designed for the YourMusic.Fun platform. The server is based on MCP standards and provides AI assistants and developers with a simple and easy-to-use music generation interface.

## Project Structure

```
yourmusic-fun-mcp/
├── yourmusic_fun_mcp/           # Core MCP server code
│   ├── __init__.py              # Package initialization file
│   ├── __main__.py              # Command line entry point
│   └── api.py                   # Core API implementation
├── tests/                       # Test code
│   └── test_api.py              # API tests
├── pyproject.toml               # Project configuration file
├── requirements.txt              # Python dependencies
├── README.md                    # Project documentation
├── claude_desktop_config_example.json  # Claude Desktop configuration example
├── install.sh                   # Installation script
├── PROJECT_STRUCTURE.md         # This file
└── LICENSE                      # MIT License
```

## Core File Descriptions

### 1. `yourmusic_fun_mcp/api.py` - Main Implementation File

This is the core of the entire MCP server, containing the following main functionalities:

#### Environment Configuration
- `YOURMUSIC_API_KEY`: YourMusic.Fun API key (required)
- `YOURMUSIC_API_URL`: API base URL (default: https://app.yourmusic.fun)
- `TIME_OUT_SECONDS`: Timeout duration (default: 600 seconds/10 minutes)
- `YOURMUSIC_MCP_BASE_PATH`: Base path for file operations

#### MCP Tools

**generate_prompt_song**: Inspiration mode song generation tool
- Parameters: prompt, instrumental, model_type, output_directory
- Functionality: Calls YourMusic.Fun API to generate music, polls status, downloads and saves files
- Support: Instrumental music generation, multiple AI model options

**generate_custom_song**: Custom mode song generation tool
- Parameters: title, lyric, model_type, tags, instrumental, vocal_gender, weirdness_constraint, style_weight, output_directory
- Functionality: Generates music based on user-specified lyrics and title
- Support: Complete music customization parameters

**play_audio**: Audio playback tool
- Parameters: input_file_path
- Functionality: Plays audio files from specified paths
- Support: Multiple audio formats

#### Helper Functions

**File Management Functions**:
- `is_file_writeable()`: Checks path writability
- `make_output_path()`: Generates output paths
- `extract_filename_from_url()`: Extracts filenames from URLs
- `check_audio_file()`: Checks audio file formats
- `handle_input_file()`: Handles input files

**API Interaction Functions**:
- `query_song_task()`: Queries song generation task status
- `play()`: Core audio playback logic

### 2. Configuration and Dependencies

#### `pyproject.toml`
- Project metadata and dependency configuration
- Defines MCP server entry points
- Specifies Python version requirements (>=3.10)
- Contains project classifications and keywords

#### `requirements.txt`
- Core dependency package list
- Includes MCP framework, audio processing, HTTP client libraries, etc.

### 3. Testing and Examples

#### `tests/test_api.py`
- Tests song generation functionality
- Tests audio playback functionality
- Includes asynchronous test support

#### `claude_desktop_config_example.json`
- Removed, configuration examples are now in README.md

## Design Features

### 1. Designed Specifically for YourMusic.Fun Platform
- Fully compatible with YourMusic.Fun API interfaces
- Uses POST `/api/music/genGptDesc` to create tasks
- Uses POST `/api/music/musicGenerate/status` to query status
- Supports instrumental and model_type parameters

### 2. Simplified Feature Set
- Focuses on core music generation functionality
- Song generation: Supports text descriptions, instrumental options, model selection
- Audio playback: Supports multiple formats, direct playback functionality

### 3. Asynchronous Processing
- Uses async/await to handle long-running tasks
- Implements intelligent polling mechanism (every 2 seconds)
- Supports configurable timeout settings (default: 10 minutes)

### 4. Comprehensive Error Handling
- Layered error handling: HTTP errors, API errors, business logic errors
- Provides clear error messages and user-friendly prompts
- Automatic retry and status checking

## Usage Workflow

1. **Configure Environment Variables**: Set API keys and configuration parameters
2. **Start MCP Server**: Run `python -m yourmusic_fun_mcp.api`
3. **Integrate with Client**: Configure in Claude Desktop or other MCP clients
4. **Use Tools**: Call song generation and audio playback functions through MCP protocol

## API Integration Workflow

### Song Generation Process
1. **Submit Task**: Call `/api/music/genGptDesc` to create generation task
2. **Get Task ID**: Extract taskId from response
3. **Poll Status**: Continuously query `/api/music/musicGenerate/status` until completion
4. **Download Files**: Download audio files after task completion
5. **Save Locally**: Save to specified directory

### Status Polling Logic
- Query task status every 2 seconds
- Supported statuses: processing, completed, error, timeout
- Automatic timeout handling (configurable)

## Extensibility

This design allows you to easily:
- Add new music generation parameters
- Integrate more YourMusic.Fun API endpoints
- Customize file saving logic
- Add new audio processing functionality
- Support more AI models

## Important Notes

1. **API Key Security**: Ensure API keys are securely passed through environment variables
2. **Timeout Configuration**: Adjust timeout settings based on YourMusic.Fun's actual response times
3. **Error Handling**: Implements comprehensive error handling with user-friendly error messages
4. **File Permissions**: Automatically checks file path writability and permissions
5. **Network Stability**: Implements retry mechanisms and status checking

## Technology Stack

- **MCP Framework**: FastMCP
- **HTTP Clients**: httpx (asynchronous), requests (synchronous)
- **Audio Processing**: sounddevice, soundfile
- **File Operations**: pathlib, os
- **Asynchronous Support**: asyncio, async/await
- **Error Handling**: Custom exception classes

## Deployment Recommendations

1. **Environment Isolation**: Use virtual environments or containers
2. **Dependency Management**: Use requirements.txt or pyproject.toml
3. **Configuration Management**: Manage sensitive information through environment variables
4. **Logging**: Enable detailed logging for debugging
5. **Monitoring**: Monitor API call frequency and response times
