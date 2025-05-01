from pypdf import PdfWriter

def merge_pdfs():
    pdfs = ['./src/data/pdf1.pdf', './src/data/pdf2.pdf', './src/data/pdf3.pdf', './src/data/pdf4.pdf']

    merger = PdfWriter()

    print("Writing to result.pdf...")
    for pdf in pdfs:
        merger.append(pdf)

    merger.write("./src/data/result.pdf")
    merger.close()
    print("Merged PDF saved sucessfully.")


merge_pdfs()
