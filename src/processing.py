import io
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from docx.opc.exceptions import PackageNotFoundError, OpcError
from zipfile import BadZipFile
from docx import Document

def extract_text(content: bytes, content_type: str) -> str:
    pdf_list = []
    word_list = []
    
    if content_type == "text/plain":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("File format must be UTF-8.")

        if not text.strip():
            raise ValueError("Extracted text is empty.")
        return text

    elif content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(content))

            for page in reader.pages:
                text = page.extract_text()

                if text is None:
                    text = ""

                pdf_list.append(text)

            full_text = "\n".join(pdf_list)

        except PdfReadError:
            raise ValueError("PDF is corrupt.")
        
        if not full_text.strip():
            raise ValueError("Extracted pdf is empty.")
        return full_text

    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            document = Document(io.BytesIO(content))

            for para in document.paragraphs:
                text = para.text
                word_list.append(text)

            full_text = "\n".join(word_list)

        except (PackageNotFoundError, OpcError, BadZipFile, KeyError):
            raise ValueError("Word is corrupt.")

        if not full_text.strip():
            raise ValueError("Extracted word is empty.")

        return full_text

    else:
        raise ValueError("Unsupported file type.")
