# Changelog

All notable changes to the YourMusic.Fun MCP Server project will be documented in this file.

## [1.0.0] - 2025-08-04

### Added
-  Initial release of YourMusic.Fun MCP Server
- 🎼 **Two AI music generation modes**:
  - **Inspiration Mode (灵感模式)**: Generate music from simple text descriptions
  - **Custom Mode (自定义模式)**: Generate music with specific lyrics, title, and style parameters
- 🔊 Audio playback tool for generated music files
- ⚙️ Configurable environment variables for API integration
- 📁 Flexible file output management with intelligent naming
-  Comprehensive test suite
- 📚 Complete documentation and examples

### Features
- **generate_prompt_song**: Generate AI music based on text prompts (inspiration mode)
  - Support for instrumental and vocal music
  - Multiple AI model options (chirp-v3-5, etc.)
  - Customizable output directories
  - Automatic file download and saving
  - AI-generated titles for output files

- **generate_custom_song**: Generate AI music with specific parameters (custom mode)
  - User-defined song title and lyrics
  - Style customization (tags, vocal gender, weirdness, style weight)
  - Support for chirp-v4 model
  - Advanced parameter control
  - Automatic file download and saving

- **play_audio**: Play audio files directly in MCP clients
  - Support for multiple audio formats
  - High-quality audio playback
  - File validation and error handling

### Technical Details
- Built with FastMCP framework
- Async/await support for long-running tasks
- Intelligent polling mechanism for API status
- Comprehensive error handling and user feedback
- File permission and path validation
- Configurable timeout settings (default: 10 minutes)
- Support for both localhost and production API endpoints

### Integration
- Claude Desktop support
- OpenAI Agents compatibility
- Standard MCP protocol compliance
- Environment-based configuration
- Multiple MCP client configurations

### Documentation
- Comprehensive README with examples for both modes
- Project structure documentation
- Installation and setup guides
- Troubleshooting and FAQ sections
- Chinese language support in tool descriptions

---

## [0.1.0] - 2025-08-18 (Legacy)

### Added
- Basic MCP server implementation
- Single song generation tool
- Audio playback functionality

---

## Development Notes

This project was created by adapting the MCP server architecture for YourMusic.Fun's specific API endpoints and requirements. It maintains the same high-quality code structure while providing a focused music generation experience with dual generation modes.

### Breaking Changes from 0.1.0 to 1.0.0
- `generate_song` tool renamed to `generate_prompt_song`
- Added new `generate_custom_song` tool
- Enhanced API response parsing
- Improved file naming logic
- Better error handling and user feedback
