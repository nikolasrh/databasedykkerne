"""
Konverter PDF-filer til markdown-tekst
"""
from pypdf import PdfReader
from pathlib import Path


def pdf_to_text(pdf_path):
    """Konverter én PDF til ren tekst"""
    reader = PdfReader(pdf_path)
    pages = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    
    return "\n\n".join(pages)


def convert_all_pdfs():
    """Konverter alle PDFs i input/ til markdown i output/"""
    input_dir = Path(__file__).parent / "input"
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"Ingen PDF-filer funnet i {input_dir}")
        return
    
    print(f"Fant {len(pdf_files)} PDF-filer")
    
    for pdf_path in pdf_files:
        print(f"Konverterer: {pdf_path.name}...")
        
        try:
            text = pdf_to_text(pdf_path)
            output_path = output_dir / f"{pdf_path.stem}.md"
            output_path.write_text(text, encoding='utf-8')
            print(f"✓ Lagret: {output_path.name}")
        except Exception as e:
            print(f"✗ Feil ved konvertering av {pdf_path.name}: {e}")
    
    print(f"\nFerdig! {len(pdf_files)} filer konvertert")


if __name__ == "__main__":
    convert_all_pdfs()
