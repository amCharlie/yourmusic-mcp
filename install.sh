#!/bin/bash

echo "🎵 Installing YourMusic.Fun MCP Server..."
echo "=========================================="

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# 检查pip是否可用
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not available. Please install pip first."
    exit 1
fi

# 安装依赖
echo "📦 Installing dependencies..."
pip3 install "mcp[cli]>=1.6.0" "sounddevice==0.5.1" "soundfile==0.13.1" "requests==2.31.0" "httpx>=0.24.0"

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# 安装MCP服务器
echo "🚀 Installing YourMusic.Fun MCP Server..."
pip3 install -e .

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install MCP server"
    exit 1
fi

echo ""
echo "🎉 Installation completed successfully!"
echo "======================================"
echo ""
echo "📋 Next steps:"
echo "1. Log in to the official website: https://app.yourmusic.fun, and contact customer support to obtain an API Key."
echo "2. Set environment variable: export YOURMUSIC_API_KEY='your-api-key-here'"
echo "3. Copy configuration from README.md examples to Claude Desktop"
echo "4. Restart Claude Desktop"
echo ""
echo "🧪 To test the installation:"
echo "python3 -m yourmusic_fun_mcp.api"
echo ""
echo "📚 For more information, see README.md"
echo ""
echo "🎵 Happy music making with YourMusic.Fun!"
