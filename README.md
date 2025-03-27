# Video & PDF Summarizer

A Django web application that automatically summarizes content from YouTube videos and PDF documents using NLP technology.

## Features

- **YouTube Video Summarization**:
  - Extracts captions from YouTube videos when available
  - Falls back to audio extraction and transcription if no captions exist
  - Works with any valid YouTube URL

- **PDF Document Summarization**:
  - Supports standard PDFs with text content
  - Includes OCR capabilities for scanned documents
  - Handles clean-up of uploaded files automatically

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **NLP Models**: 
  - BART (facebook/bart-large-cnn) for summarization
  - Whisper for audio transcription
- **Video Processing**: yt-dlp
- **PDF Processing**: PyMuPDF, pytesseract, pdf2image

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Video_PDF_Sum

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    
4. Start the Django development server:
    ```bash 
    python manage.py runserver
