import yt_dlp
import whisper
import os
import re

import pymupdf
import pytesseract
from pdf2image import convert_from_path

def is_youtube_url(url):
    """Check if the URL is a YouTube URL."""
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    return bool(re.match(youtube_regex, url))

def get_youtube_captions(video_url):
    """Extract captions from YouTube video if available."""
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Check if subtitles are available
            if info.get('subtitles') and 'en' in info['subtitles']:
                # Get English subtitles
                subtitles = info['subtitles']['en']
                for subtitle in subtitles:
                    if subtitle.get('ext') == 'vtt':
                        subtitle_url = subtitle['url']
                        # Download the subtitle content
                        import requests
                        response = requests.get(subtitle_url)
                        if response.status_code == 200:
                            # Parse VTT file to extract text
                            import webvtt
                            vtt_content = response.text
                            temp_file = "temp_subtitle.vtt"
                            with open(temp_file, "w", encoding="utf-8") as f:
                                f.write(vtt_content)
                            
                            captions = []
                            for caption in webvtt.read(temp_file):
                                captions.append(caption.text)
                            
                            os.remove(temp_file)
                            return " ".join(captions)
            
            # If manual subtitles not found, try automatic captions
            if info.get('automatic_captions') and 'en' in info['automatic_captions']:
                subtitles = info['automatic_captions']['en']
                for subtitle in subtitles:
                    if subtitle.get('ext') == 'vtt':
                        # Similar process as above
                        subtitle_url = subtitle['url']
                        import requests
                        response = requests.get(subtitle_url)
                        if response.status_code == 200:
                            import webvtt
                            vtt_content = response.text
                            temp_file = "temp_subtitle.vtt"
                            with open(temp_file, "w", encoding="utf-8") as f:
                                f.write(vtt_content)
                            
                            captions = []
                            for caption in webvtt.read(temp_file):
                                captions.append(caption.text)
                            
                            os.remove(temp_file)
                            return " ".join(captions)
        
        return None
    except Exception as e:
        print(f"Error fetching captions: {str(e)}")
        return None

def extract_audio_from_youtube(video_url, output_path="media/audio"):
    """Downloads audio from YouTube video."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return f"{output_path}.mp3"

def transcribe_audio(audio_path):
    """Uses Whisper to transcribe audio."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]






def extract_text_from_pdf(pdf_path):
    """Extracts text from normal PDFs."""
    print(f"Extracting text from PDF: {pdf_path}")
    doc = pymupdf.open(pdf_path)
    return "\n".join([page.get_text() for page in doc])

def extract_text_from_scanned_pdf(pdf_path):
    """Extracts text from scanned PDFs using OCR."""
    pages = convert_from_path(pdf_path)
    text = "\n".join([pytesseract.image_to_string(page) for page in pages])
    return text

