from gtts import gTTS
import PyPDF2
import os

cur_file_dir = os.path.dirname(__file__)

def pdf_to_text(pdf_path):
    my_text = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                my_text.append(page_text)
    return "\n".join(my_text)

pdf_path = os.path.join(cur_file_dir, "random_pdf.pdf")
text_from_pdf = pdf_to_text(pdf_path)

if not text_from_pdf.strip():
    text_from_pdf = "Hello, this is a Python text to speech example!"

language = 'en'
tts = gTTS(text=text_from_pdf, lang=language, slow=False)
tts.save("welcome.mp3")
os.system("start welcome.mp3")

