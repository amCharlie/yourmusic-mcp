# api.py
import os
import sys
import time
import httpx
import requests
from pathlib import Path
from datetime import datetime
from typing import Iterator, Union
from urllib.parse import urlparse
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

mcp = FastMCP("YourMusic.Fun")
# setup API key，for calling YourMusic.Fun API
# os.environ["YOURMUSIC_API_KEY"] = "<YOURMUSIC_API_KEY>"
api_key = os.getenv('YOURMUSIC_API_KEY')
global_base_path = os.getenv("YOURMUSIC_MCP_BASE_PATH")
api_url = os.getenv('YOURMUSIC_API_URL')
if api_url is None:
    api_url = "https://app.yourmusic.fun"

default_time_out = 600.0  # seconds, 10 minutes as per YourMusic.Fun API
time_out_env = os.getenv('TIME_OUT_SECONDS')
if time_out_env is not None:
    default_time_out = float(time_out_env)


def is_file_writeable(path: Path) -> bool:
    """检查路径是否可写"""
    if path.exists():
        return os.access(path, os.W_OK)
    parent_dir = path.parent
    return os.access(parent_dir, os.W_OK)


def make_output_path(
        output_directory: str | None, base_path: str | None = None
) -> Path:
    """生成输出路径，如果未指定则默认保存到桌面"""
    output_path = None
    if output_directory is None:
        output_path = Path.home() / "Desktop"
    elif not os.path.isabs(output_directory) and base_path:
        output_path = Path(os.path.expanduser(base_path)) / Path(output_directory)
    else:
        output_path = Path(os.path.expanduser(output_directory))
    
    if not is_file_writeable(output_path):
        raise Exception(f"Directory ({output_path}) is not writeable")
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def extract_filename_from_url(url):
    """从URL中提取文件名"""
    parsed_url = urlparse(url)
    filename = parsed_url.path.split('/')[-1]
    return filename


def check_audio_file(path: Path) -> bool:
    """检查文件是否为支持的音频格式"""
    audio_extensions = {
        ".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac", 
        ".mp4", ".avi", ".mov", ".wmv",
    }
    return path.suffix.lower() in audio_extensions


def handle_input_file(file_path: str, audio_content_check: bool = True) -> Path:
    """处理输入文件路径，验证文件存在性和格式"""
    if not os.path.isabs(file_path) and not os.environ.get("YOURMUSIC_MCP_BASE_PATH"):
        raise Exception(
            "File path must be an absolute path if YOURMUSIC_MCP_BASE_PATH is not set"
        )
    
    path = Path(file_path)
    if not path.exists() and path.parent.exists():
        raise Exception(f"File ({path}) does not exist")
    elif not path.exists():
        raise Exception(f"File ({path}) does not exist")
    elif not path.is_file():
        raise Exception(f"File ({path}) is not a file")

    if audio_content_check and not check_audio_file(path):
        raise Exception(f"File ({path}) is not an audio or video file")
    return path


@mcp.tool(
    description="""🎼 Inspiration Mode: Generate songs based on simple text descriptions (AI automatically generates title, lyrics, style, etc.)
    
    Use case: Use when users only provide simple song themes or emotional descriptions without detailed specifications for song name, lyrics, style, and other specific parameters.
    
    Example inputs:
    - "Help me generate a song about a peaceful morning"
    - "Want a song that expresses longing"
    - "Create music about friendship"
    
    ⚠️ COST WARNING: This tool makes an API call to YourMusic.Fun which may incur costs. Only use when explicitly requested by the user.
    
    Language Note: When calling this method, please pass the prompt in the corresponding language version based on the user's input language.
    
    Args:
        prompt (str): Song theme or emotional description, 1-1200 characters. Example: "Song about peaceful morning", "Song expressing longing"
        instrumental (bool, optional): Whether instrumental only, default False (with vocals)
        model_type (str, optional): AI model type, default 'chirp-v3-5'
        output_directory (str, optional): Save directory, default saves to desktop
    
    Returns:
        Generated song file list, filename format: title1.mp3, title2.mp3
    """
)
async def generate_prompt_song(prompt: str, instrumental: bool = False, model_type: str = "chirp-v3-5", output_directory: str | None = None) -> list[TextContent]:
    try:
        if not api_key:
            raise Exception("Cannot find API key. Please set YOURMUSIC_API_KEY environment variable.")
        
        if not prompt or prompt.strip() == "":
            raise Exception("Prompt text is required.")
        
        if len(prompt.strip()) > 1200:
            raise Exception("Prompt text must be less than 1200 characters.")
        
        output_path = make_output_path(output_directory, global_base_path)
        
        url = f"{api_url}/generate/prompt"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            "prompt": prompt,
            "instrumental": instrumental,
            "model_type": model_type,
            "albumId": None 
        }
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.post(url, json=params, headers=headers)
            response.raise_for_status()
            result = response.json()
        
        # 解析结果，获取任务ID
        if not result or result.get("code") != 200:
            error_msg = result.get("message", "Unknown error") if result else "No response"
            raise Exception(f"Failed to create song generation task: {error_msg}")
        
        # 从返回结果中提取任务ID
        songs_data = result.get("data", {}).get("data", [])
        if not songs_data:
            raise Exception("No songs data returned from API")
        
        # 从第一个歌曲数据中获取taskId
        task_id = songs_data[0].get("taskId")
        if not task_id:
            raise Exception("No task ID returned from API")
        
        print(f"Song generation task created successfully. Task ID: {task_id}")
        
        # 轮询查询任务状态直到完成
        current_timestamp = datetime.now().timestamp()
        while True:
            if (datetime.now().timestamp() - current_timestamp) > default_time_out:
                raise Exception(f"Song generation timed out after {default_time_out} seconds")
            
            songs, status = await query_song_task(task_id)
            
            if status == "error":
                raise Exception(f"Song generation failed with error status")
            elif status == "timeout":
                raise Exception("Song generation timed out")
            elif status == "completed" or status == "success":
                break
            else:
                time.sleep(2)
        
        # 下载并保存歌曲文件
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_path_group = []
        
        for i, song in enumerate(songs, 1):
            song_url = song.get("audio_url") or song.get("url") or song.get("audioUrl") or song.get("downloadUrl")
            if not song_url:
                continue
                
            song_title = song.get("title", "").strip()
            if song_title:
                filename = f"{song_title}{i}.mp3"
            else:
                filename = f"歌曲{i}.mp3"
            
            response = requests.get(song_url)
            if response.status_code == 200:
                song_bytes = response.content
            else:
                raise Exception(f"Failed to download song from {song_url}")
            
            save_path = output_path / filename
            with open(save_path, "wb") as f:
                f.write(song_bytes)
            save_path_group.append(save_path)
        
        if not save_path_group:
            raise Exception("No songs were downloaded successfully")
        
        return [TextContent(
            type="text",
            text=f"Success! Song generated and saved as: {save_path}",
        ) for save_path in save_path_group]
        
    except Exception as e:
        print(f"Error details: {e}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        raise Exception(f"Request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e


@mcp.tool(
    description="""🎵 Custom Mode: Generate songs based on detailed song information (user specifies song name, lyrics, style, and other specific parameters)
    
    Use case: Use when users provide detailed song information including song name, lyrics, style, vocal gender, and other specific parameters.
    
    Example inputs:
    - Contains song name, complete lyrics, style requirements, and other detailed information
    - Example: "Song name: Summer of Cicada Shedding, Lyrics: [complete lyrics], use male voice, style use folk"
    
    ⚠️ COST WARNING: This tool makes an API call to YourMusic.Fun which may incur costs. Only use when explicitly requested by the user.
    
    Language Note: When calling this method, please pass the title and lyrics in the corresponding language version based on the user's input language.
    
    Args:
        title (str): Song title, example: "Summer of Cicada Shedding"
        lyric (str): Complete lyrics content, supports multi-paragraph lyrics format
        model_type (str, optional): AI model type, default 'chirp-v4'
        tags (str, optional): Music style tags, example: 'pop', 'rock', 'jazz', 'folk'
        instrumental (bool, optional): Whether instrumental only, default False (with vocals)
        vocal_gender (str, optional): Vocal gender, 'm' for male, 'f' for female, default 'm'
        weirdness_constraint (float, optional): Weirdness constraint, 0.0-1.0, default 0.6
        style_weight (float, optional): Style weight, 0.0-1.0, default 0.7
        output_directory (str, optional): Save directory, default saves to desktop
    
    Returns:
        Generated song file list, filename format: title1.mp3, title2.mp3
    """
)
async def generate_custom_song(
    title: str, 
    lyric: str, 
    model_type: str = "chirp-v4", 
    tags: str = "pop", 
    instrumental: bool = False, 
    vocal_gender: str = "m", 
    weirdness_constraint: float = 0.6, 
    style_weight: float = 0.7, 
    output_directory: str | None = None
) -> list[TextContent]:
    try:
        if not api_key:
            raise Exception("Cannot find API key. Please set YOURMUSIC_API_KEY environment variable.")
        
        if not title or title.strip() == "":
            raise Exception("Title is required.")
        
        if not lyric or lyric.strip() == "":
            raise Exception("Lyrics are required.")
        
        output_path = make_output_path(output_directory, global_base_path)
        
        # 调用自定义歌曲生成 API
        url = f"{api_url}/generate/custom"
        
        # 设置请求参数
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        params = {
            "model_type": model_type,
            "lyric": lyric,
            "title": title,
            "tags": tags,
            "instrumental": instrumental,
            "vocalGender": vocal_gender,
            "weirdnessConstraint": weirdness_constraint,
            "styleWeight": style_weight
        }
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.post(url, json=params, headers=headers)
            response.raise_for_status()
            result = response.json()
        
        # 解析结果，获取任务ID
        if not result or result.get("code") != 200:
            error_msg = result.get("message", "Unknown error") if result else "No response"
            raise Exception(f"Failed to create custom song generation task: {error_msg}")
        
        # 从返回结果中提取任务ID
        songs_data = result.get("data", {}).get("data", [])
        if not songs_data:
            raise Exception("No songs data returned from API")
        
        # 从第一个歌曲数据中获取taskId
        task_id = songs_data[0].get("taskId")
        if not task_id:
            raise Exception("No task ID returned from API")
        
        print(f"Custom song generation task created successfully. Task ID: {task_id}")
        
        # 轮询查询任务状态直到完成
        current_timestamp = datetime.now().timestamp()
        while True:
            if (datetime.now().timestamp() - current_timestamp) > default_time_out:
                raise Exception(f"Custom song generation timed out after {default_time_out} seconds")
            
            songs, status = await query_song_task(task_id)
            
            if status == "error":
                raise Exception(f"Custom song generation failed with error status")
            elif status == "timeout":
                raise Exception("Custom song generation timed out")
            elif status == "completed" or status == "success":
                break
            else:
                # 等待2秒后重试
                time.sleep(2)
        
        # 下载并保存歌曲文件
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_path_group = []
        
        for i, song in enumerate(songs, 1):
            song_url = song.get("audio_url") or song.get("url") or song.get("audioUrl") or song.get("downloadUrl")
            if not song_url:
                continue
                
            song_title = song.get("title", "").strip()
            if song_title:
                filename = f"{song_title}{i}.mp3"
            else:
                filename = f"{title}{i}.mp3"
            
            # 下载歌曲文件
            response = requests.get(song_url)
            if response.status_code == 200:
                song_bytes = response.content
            else:
                raise Exception(f"Failed to download song from {song_url}")
            
            save_path = output_path / filename
            with open(save_path, "wb") as f:
                f.write(song_bytes)
            save_path_group.append(save_path)
        
        if not save_path_group:
            raise Exception("No songs were downloaded successfully")
        
        return [TextContent(
            type="text",
            text=f"Success! Custom song '{title}' generated and saved as: {save_path}",
        ) for save_path in save_path_group]
        
    except Exception as e:
        print(f"Error details: {e}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        raise Exception(f"Custom song generation failed: {str(e)}") from e


async def query_song_task(task_id: str) -> (list, str):
    """查询歌曲生成任务状态"""
    try:
        url = f"{api_url}/generate/status"
        headers = {'Authorization': f'Bearer {api_key}'}
        
        # 根据API接口，需要发送POST请求，body包含taskId
        params = {"taskId": task_id}
        
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.post(url, json=params, headers=headers)
            response.raise_for_status()
            result = response.json()

        if not result or result.get("code") != 200:
            return [], "error"
        
        # 检查是否有歌曲数据
        songs = result.get("data", [])
        if songs and len(songs) > 0:
            # 检查所有歌曲的状态
            all_complete = True
            any_error = False
            
            for song in songs:
                status = song.get("status", "unknown")
                if status == "error":
                    any_error = True
                    break
                elif status != "complete":
                    all_complete = False
            
            if any_error:
                return songs, "error"
            elif all_complete:
                return songs, "completed"
            else:
                return songs, "processing"
        else:
            return [], "processing"
            
    except Exception as e:
        print(f"Error details: {e}")
        print(f"Error type: {type(e)}")
        if hasattr(e, 'response'):
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        raise Exception(f"Request failed: {str(e)}") from e


def play(
        audio: Union[bytes, Iterator[bytes]]
) -> None:
    """播放音频数据"""
    if isinstance(audio, Iterator):
        audio = b"".join(audio)

    try:
        import io
        import sounddevice as sd  # type: ignore
        import soundfile as sf  # type: ignore
    except ModuleNotFoundError:
        message = (
            "`pip install sounddevice soundfile` required for audio playback"
        )
        raise ValueError(message)
    
    sd.play(*sf.read(io.BytesIO(audio)))
    sd.wait()


@mcp.tool(description="Play an audio file. Supports WAV, MP3, M4A, AAC, OGG, FLAC, MP4, AVI, MOV, WMV formats.")
def play_audio(input_file_path: str) -> TextContent:
    """播放音频文件的MCP工具"""
    file_path = handle_input_file(input_file_path)
    play(open(file_path, "rb").read())
    return TextContent(type="text", text=f"Successfully played audio file: {file_path}")


def main():
    """运行MCP服务器"""
    print("Starting YourMusic.Fun MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
