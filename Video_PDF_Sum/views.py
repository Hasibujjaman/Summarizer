from django.shortcuts import render
from django.http import JsonResponse
import os
from .utils import extract_audio_from_youtube, transcribe_audio, is_youtube_url, get_youtube_captions, extract_text_from_pdf
from .chatmodel import summarize_text
from django.views.decorators.csrf import csrf_exempt  # Add this import

def summarize_youtube(request):
    video_url = request.GET.get("url")
    if not video_url:
        return JsonResponse({"error": "No URL provided"}, status=400)

    text = None
    
    # First check if it's a YouTube URL
    if is_youtube_url(video_url):
        # Try to get captions first
        print("Trying to get YouTube captions...")
        text = get_youtube_captions(video_url)
    
    # If no captions were found or it's not a YouTube URL, fall back to audio extraction
    if not text:
        print("No captions found or not a YouTube URL. Extracting audio...")
        audio_path = extract_audio_from_youtube(video_url)
        text = transcribe_audio(audio_path)
    
    print(text)
    summary = summarize_text(text)
    
    return JsonResponse({"summary": summary})

@csrf_exempt  # Add this decorator to exempt this view from CSRF protection
def summarize_pdf(request):
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf = request.FILES["pdf"]
        
        # Create media directory if it doesn't exist
        media_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')
        os.makedirs(media_dir, exist_ok=True)
        
        # Create a more robust path
        pdf_path = os.path.join(media_dir, pdf.name)
        print(f"PDF file saved at: {pdf_path}")

        # Save the uploaded file
        with open(pdf_path, "wb") as f:
            for chunk in pdf.chunks():
                f.write(chunk)

        try:
            # Extract text and summarize
            text = extract_text_from_pdf(pdf_path)
            summary = summarize_text(text)
            
            return JsonResponse({"summary": summary})
        finally:
            # Clean up the file after processing
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    return JsonResponse({"error": "No file uploaded"}, status=400)

def homePage(request):
    return render(request, "home.html")

