
from django.shortcuts import render
from django.http import JsonResponse
from .utils import extract_audio_from_youtube, transcribe_audio
from .chatmodel import summarize_text

def summarize_youtube(request):
    video_url = request.GET.get("url")
    if not video_url:
        return JsonResponse({"error": "No URL provided"}, status=400)

    audio_path = extract_audio_from_youtube(video_url)
    text = transcribe_audio(audio_path)
    print(text)
    summary = summarize_text(text)
    
    print(summary)

    return JsonResponse({"summary": summary})

# def summarize_pdf(request):
#     if request.method == "POST" and request.FILES.get("pdf"):
#         pdf = request.FILES["pdf"]
#         pdf_path = f"media/{pdf.name}"

#         with open(pdf_path, "wb") as f:
#             for chunk in pdf.chunks():
#                 f.write(chunk)

#         text = extract_text_from_pdf(pdf_path)
#         summary = summarize_text(text)

#         return JsonResponse({"summary": summary})
    
#     return JsonResponse({"error": "No file uploaded"}, status=400)


def homePage(request):

    return render(request, "home.html")

