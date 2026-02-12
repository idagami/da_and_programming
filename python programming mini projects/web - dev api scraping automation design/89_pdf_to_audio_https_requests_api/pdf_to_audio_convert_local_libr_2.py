import pyttsx3
import os
import PyPDF2

def pdf_to_text(pdf_path):
    text = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

def text_to_speech(text, output_mp3):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_mp3)
    engine.runAndWait()
    print(f"Audio written to {output_mp3}")


if __name__ == "__main__":
    cur_file_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(cur_file_dir, "random_pdf.pdf")

    text = pdf_to_text(pdf_path)

    if text.strip():
        text_to_speech(text, os.path.join(cur_file_dir, "output.mp3"))
    else:
        print("No text found in PDF.")
