import yt_dlp
import whisper
import os

# import fitz  # PyMuPDF
# import pytesseract
# from pdf2image import convert_from_path

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



# def extract_text_from_pdf(pdf_path):
#     """Extracts text from normal PDFs."""
#     doc = fitz.open(pdf_path)
#     return "\n".join([page.get_text() for page in doc])

# def extract_text_from_scanned_pdf(pdf_path):
#     """Extracts text from scanned PDFs using OCR."""
#     pages = convert_from_path(pdf_path)
#     text = "\n".join([pytesseract.image_to_string(page) for page in pages])
#     return text

