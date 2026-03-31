"""
Utility script to merge PDF data files into a single result.pdf.
Run this before rag_loader if you have new PDF files.
"""
from pypdf import PdfWriter
from core.config import DATA_DIR


def merge_pdfs():
    pdfs = [
        DATA_DIR / "pdf1.pdf",
        DATA_DIR / "pdf2.pdf",
        DATA_DIR / "pdf3.pdf",
        DATA_DIR / "pdf4.pdf",
    ]

    merger = PdfWriter()

    print("Writing to result.pdf...")
    for pdf in pdfs:
        if pdf.exists():
            merger.append(str(pdf))
        else:
            print(f"Warning: {pdf} not found, skipping.")

    output_path = DATA_DIR / "result.pdf"
    merger.write(str(output_path))
    merger.close()
    print("Merged PDF saved successfully.")


if __name__ == "__main__":
    merge_pdfs()
