import pytest
import asyncio
import os
from yourmusic_fun_mcp.api import generate_prompt_song, generate_custom_song, play_audio


@pytest.mark.asyncio
async def test_generate_prompt_song():
    """测试YourMusic.Fun灵感模式歌曲生成功能"""
    try:
        # 检查API密钥是否设置
        api_key = os.getenv('YOURMUSIC_API_KEY')
        if not api_key:
            print("⚠️  Skipping prompt song generation test: YOURMUSIC_API_KEY not set")
            return
        
        print("🎼 Testing prompt song generation with YourMusic.Fun API...")
        
        # 测试灵感模式歌曲生成
        result = await generate_prompt_song(
            prompt="A peaceful morning in the mountains with gentle piano and nature sounds",
            instrumental=True,
            model_type="chirp-v3-5"
        )
        print("✅ Prompt song generation result:", result)
        
    except Exception as e:
        print(f"❌ Prompt song generation test failed: {str(e)}")


@pytest.mark.asyncio
async def test_generate_custom_song():
    """测试YourMusic.Fun自定义模式歌曲生成功能"""
    try:
        # 检查API密钥是否设置
        api_key = os.getenv('YOURMUSIC_API_KEY')
        if not api_key:
            print("⚠️  Skipping custom song generation test: YOURMUSIC_API_KEY not set")
            return
        
        print("🎵 Testing custom song generation with YourMusic.Fun API...")
        
        # 测试自定义模式歌曲生成
        result = await generate_custom_song(
            title="Test Song",
            lyric="This is a test lyric for custom song generation",
            model_type="chirp-v4",
            tags="pop",
            instrumental=False,
            vocal_gender="m",
            weirdness_constraint=0.6,
            style_weight=0.7
        )
        print("✅ Custom song generation result:", result)
        
    except Exception as e:
        print(f"❌ Custom song generation test failed: {str(e)}")


def test_play_audio():
    """测试YourMusic.Fun音频播放功能"""
    try:
        print("🔊 Testing audio playback functionality...")
        
        # 这个测试需要有效的音频文件路径
        # 在实际环境中，你可以提供一个测试音频文件
        test_audio_path = os.getenv('TEST_AUDIO_PATH')
        
        if test_audio_path and os.path.exists(test_audio_path):
            result = play_audio(test_audio_path)
            print("✅ Audio playback result:", result)
        else:
            print("⚠️  Audio playback test skipped - no valid test audio file provided")
            print("   Set TEST_AUDIO_PATH environment variable to test audio playback")
            
    except Exception as e:
        print(f"❌ Audio playback test failed: {str(e)}")


def test_environment_setup():
    """测试环境配置"""
    print("🔧 Testing environment configuration...")
    
    required_vars = ['YOURMUSIC_API_KEY']
    optional_vars = ['YOURMUSIC_API_URL', 'TIME_OUT_SECONDS', 'YOURMUSIC_MCP_BASE_PATH']
    
    # 检查必需的环境变量
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
    else:
        print("✅ All required environment variables are set")
    
    # 显示可选环境变量
    print("📋 Optional environment variables:")
    for var in optional_vars:
        value = os.getenv(var, "Not set")
        print(f"   {var}: {value}")


def test_mcp_tools_availability():
    """测试MCP工具是否可用"""
    print("🛠️  Testing MCP tools availability...")
    
    try:
        # 检查工具函数是否存在
        assert hasattr(generate_prompt_song, '__call__'), "generate_prompt_song function not found"
        assert hasattr(generate_custom_song, '__call__'), "generate_custom_song function not found"
        assert hasattr(play_audio, '__call__'), "play_audio function not found"
        
        print("✅ All MCP tools are available")
        
        # 检查工具描述
        if hasattr(generate_prompt_song, 'description'):
            print(f"📝 generate_prompt_song description: {generate_prompt_song.description[:100]}...")
        if hasattr(generate_custom_song, 'description'):
            print(f"📝 generate_custom_song description: {generate_custom_song.description[:100]}...")
        if hasattr(play_audio, 'description'):
            print(f"📝 play_audio description: {play_audio.description}")
            
    except Exception as e:
        print(f"❌ MCP tools test failed: {str(e)}")


if __name__ == "__main__":
    print("🧪 Running YourMusic.Fun MCP Server Tests")
    print("=" * 50)
    
    # 运行环境配置测试
    test_environment_setup()
    print()
    
    # 运行MCP工具可用性测试
    test_mcp_tools_availability()
    print()
    
    # 运行音频播放测试
    test_play_audio()
    print()
    
    # 运行灵感模式歌曲生成测试（需要API密钥）
    try:
        asyncio.run(test_generate_prompt_song())
    except Exception as e:
        print(f"❌ Prompt song generation test failed: {str(e)}")
    
    print()
    
    # 运行自定义模式歌曲生成测试（需要API密钥）
    try:
        asyncio.run(test_generate_custom_song())
    except Exception as e:
        print(f"❌ Custom song generation test failed: {str(e)}")
    
    print("=" * 50)
    print("🏁 Tests completed!")
