# YourMusic.Fun MCP Server - Project Structure

## 项目概述

这是一个专门为YourMusic.Fun平台设计的Model Context Protocol (MCP)音乐生成服务器。该服务器基于MCP标准，为AI助手和开发者提供简单易用的音乐生成接口。

## 项目结构

```
yourmusic-fun-mcp/
├── yourmusic_fun_mcp/           # 核心MCP服务器代码
│   ├── __init__.py              # 包初始化文件
│   ├── __main__.py              # 命令行入口点
│   └── api.py                   # 核心API实现
├── tests/                       # 测试代码
│   └── test_api.py              # API测试
├── pyproject.toml               # 项目配置文件
├── requirements.txt              # Python依赖
├── README.md                    # 项目文档
├── claude_desktop_config_example.json  # Claude Desktop配置示例
├── install.sh                   # 安装脚本
├── PROJECT_STRUCTURE.md         # 本文件
└── LICENSE                      # MIT许可证
```

## 核心文件说明

### 1. `yourmusic_fun_mcp/api.py` - 主要实现文件

这是整个MCP服务器的核心，包含以下主要功能：

#### 环境配置
- `YOURMUSIC_API_KEY`: YourMusic.Fun API密钥（必需）
- `YOURMUSIC_API_URL`: API基础URL (默认: https://app.yourmusic.fun)
- `TIME_OUT_SECONDS`: 超时时间 (默认: 600秒/10分钟)
- `YOURMUSIC_MCP_BASE_PATH`: 文件操作基础路径

#### MCP工具

**generate_prompt_song**: 灵感模式歌曲生成工具
- 参数: prompt, instrumental, model_type, output_directory
- 功能: 调用YourMusic.Fun API生成音乐，轮询状态，下载并保存文件
- 支持: 纯音乐生成、多种AI模型选择

**generate_custom_song**: 自定义模式歌曲生成工具
- 参数: title, lyric, model_type, tags, instrumental, vocal_gender, weirdness_constraint, style_weight, output_directory
- 功能: 根据用户指定的歌词和标题生成音乐
- 支持: 完整的音乐定制参数

**play_audio**: 音频播放工具
- 参数: input_file_path
- 功能: 播放指定路径的音频文件
- 支持: 多种音频格式

#### 辅助函数

**文件管理函数**:
- `is_file_writeable()`: 检查路径可写性
- `make_output_path()`: 生成输出路径
- `extract_filename_from_url()`: 从URL提取文件名
- `check_audio_file()`: 检查音频文件格式
- `handle_input_file()`: 处理输入文件

**API交互函数**:
- `query_song_task()`: 查询歌曲生成任务状态
- `play()`: 音频播放核心逻辑

### 2. 配置和依赖

#### `pyproject.toml`
- 项目元数据和依赖配置
- 定义了MCP服务器的入口点
- 指定了Python版本要求 (>=3.10)
- 包含项目分类和关键词

#### `requirements.txt`
- 核心依赖包列表
- 包含MCP框架、音频处理、HTTP客户端等

### 3. 测试和示例

#### `tests/test_api.py`
- 测试歌曲生成功能
- 测试音频播放功能
- 包含异步测试支持

#### `claude_desktop_config_example.json`
- 已移除，配置示例现在在 README.md 中

## 设计特点

### 1. 专为YourMusic.Fun平台设计
- 完全适配YourMusic.Fun的API接口
- 使用POST `/api/music/genGptDesc` 创建任务
- 使用POST `/api/music/musicGenerate/status` 查询状态
- 支持instrumental和model_type参数

### 2. 简化的功能集
- 专注于核心音乐生成功能
- 歌曲生成：支持文本描述、纯音乐选项、模型选择
- 音频播放：支持多种格式、直接播放功能

### 3. 异步处理
- 使用async/await处理长时间运行的任务
- 实现了智能的轮询机制（每2秒查询一次）
- 支持可配置的超时时间（默认10分钟）

### 4. 完善的错误处理
- 分层错误处理：HTTP错误、API错误、业务逻辑错误
- 提供清晰的错误信息和用户友好的提示
- 自动重试和状态检查

## 使用流程

1. **配置环境变量**: 设置API密钥和配置参数
2. **启动MCP服务器**: 运行`python -m yourmusic_fun_mcp.api`
3. **集成到客户端**: 在Claude Desktop或其他MCP客户端中配置
4. **使用工具**: 通过MCP协议调用歌曲生成和音频播放功能

## API集成流程

### 歌曲生成流程
1. **提交任务**: 调用`/api/music/genGptDesc`创建生成任务
2. **获取任务ID**: 从响应中提取taskId
3. **轮询状态**: 持续查询`/api/music/musicGenerate/status`直到完成
4. **下载文件**: 任务完成后下载音频文件
5. **保存本地**: 保存到指定目录

### 状态轮询逻辑
- 每2秒查询一次任务状态
- 支持的状态：processing, completed, error, timeout
- 自动超时处理（可配置）

## 扩展性

这个设计允许你轻松地：
- 添加新的音乐生成参数
- 集成更多的YourMusic.Fun API端点
- 自定义文件保存逻辑
- 添加新的音频处理功能
- 支持更多的AI模型

## 注意事项

1. **API密钥安全**: 确保API密钥通过环境变量安全传递
2. **超时配置**: 根据YourMusic.Fun的实际响应时间调整超时设置
3. **错误处理**: 实现了完善的错误处理和用户友好的错误信息
4. **文件权限**: 自动检查文件路径的可写性和权限
5. **网络稳定性**: 实现了重试机制和状态检查

## 技术栈

- **MCP框架**: FastMCP
- **HTTP客户端**: httpx (异步), requests (同步)
- **音频处理**: sounddevice, soundfile
- **文件操作**: pathlib, os
- **异步支持**: asyncio, async/await
- **错误处理**: 自定义异常类

## 部署建议

1. **环境隔离**: 使用虚拟环境或容器
2. **依赖管理**: 使用requirements.txt或pyproject.toml
3. **配置管理**: 通过环境变量管理敏感信息
4. **日志记录**: 启用详细日志以便调试
5. **监控**: 监控API调用频率和响应时间
