"""YouTube audio download module."""

import os
import tempfile
import yt_dlp
from typing import Optional


def search_and_download(song_name: str, output_dir: Optional[str] = None) -> str:
    """
    Search for a song on YouTube and download its audio.
    
    Args:
        song_name: Name of the song to search for
        output_dir: Directory to save the audio file. If None, uses temp directory.
        
    Returns:
        Path to the downloaded audio file (WAV format)
        
    Raises:
        Exception: If download fails or no results found
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
    }
    
    # Search and download
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Search for the song
            print(f"Searching for: {song_name}")
            search_results = ydl.extract_info(
                f"ytsearch1:{song_name}",
                download=False
            )
            
            if not search_results or 'entries' not in search_results:
                raise Exception("No results found for the song")
            
            video = search_results['entries'][0]
            if not video:
                raise Exception("No video found for the song")
            
            # Get video URL or construct from ID
            video_url = video.get('webpage_url') or video.get('url')
            if not video_url:
                video_id = video.get('id')
                if video_id:
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                else:
                    raise Exception("Could not determine video URL")
            
            video_title = video.get('title', 'Unknown')
            print(f"Found: {video_title}")
            print(f"Downloading audio...")
            
            # Download the audio using the video URL
            # We need to create a new instance with download enabled
            ydl_opts_download = ydl_opts.copy()
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
                ydl_download.download([video_url])
            
            # Find the downloaded file
            audio_file = os.path.join(output_dir, 'audio.wav')
            if not os.path.exists(audio_file):
                # Try to find any audio file in the directory
                files = os.listdir(output_dir)
                audio_files = [f for f in files if f.endswith(('.wav', '.mp3', '.m4a'))]
                if audio_files:
                    audio_file = os.path.join(output_dir, audio_files[0])
                else:
                    raise Exception("Audio file not found after download")
            
            print(f"Downloaded: {audio_file}")
            return audio_file
            
        except Exception as e:
            raise Exception(f"Failed to download audio: {str(e)}")

