from weasyprint import HTML
from PyPDF2 import PdfMerger
from pdf2image import convert_from_path
from pytesseract import image_to_string
from fpdf import FPDF
import os
from werkzeug.utils import secure_filename
from PIL import Image
import logging

# Diretório para armazenar PDFs e imagens temporárias
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DIR_PDF = './documents'
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# Garantir que o diretório de documentos exista
os.makedirs(DIR_PDF, exist_ok=True)

def convert_html_to_pdf(html, name_file):
    """
    Converte HTML para PDF e salva no diretório 'documents'.
    """
    output_path = os.path.join(DIR_PDF, f'{name_file}.pdf')
    HTML(string=html).write_pdf(output_path)
    print(f"PDF gerado em: {output_path}")
    return name_file + ".pdf"


def merge_pdfs(pdf_files, output_name):
    """
    Mescla múltiplos PDFs e salva no diretório 'documents'.
    """
    merger = PdfMerger()
    for pdf_file in pdf_files:
        pdf_path = os.path.join(DIR_PDF, secure_filename(pdf_file.filename))
        pdf_file.save(pdf_path)
        merger.append(pdf_path)

    # Adiciona a extensão .pdf ao nome do arquivo de saída, se não estiver presente
    if not output_name.lower().endswith('.pdf'):
        output_name += '.pdf'
    
    output_path = os.path.join(DIR_PDF, output_name)
    merger.write(output_path)
    merger.close()
    print(f"PDFs mesclados em: {output_path}")
    
    return output_name  # Retorna apenas o nome do arquivo, sem o caminho


# Configurar logging
logging.basicConfig(level=logging.INFO)


def process_file_with_ocr_and_save(file, output_name=None):
    """
    Processa um arquivo (PDF ou imagem) com OCR, retorna o texto extraído e salva em um novo PDF.
    :param file: Caminho do arquivo de entrada (PDF ou imagem).
    :param output_name: Nome para o arquivo PDF de saída (opcional).
    :return: Nome do PDF gerado.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Determinar o nome do arquivo de saída com base no arquivo original
    if output_name is None:
        output_name = os.path.splitext(os.path.basename(file))[0] + "_ocr.pdf"
    else:
        output_name = os.path.splitext(os.path.basename(output_name))[0] + ".pdf"

    logging.info(f"Nome do arquivo de saída: {output_name}")

    # Criar um objeto FPDF
    pdf_writer = FPDF()
    pdf_writer.set_auto_page_break(auto=True, margin=15)
    pdf_writer.add_page()
    pdf_writer.set_font("Arial", size=12)

    extracted_text = ""

    try:
        # Verificar se é um arquivo PDF ou imagem
        if file.lower().endswith('.pdf'):
            logging.info("Processando PDF")
            # Processar cada página do PDF
            try:
                pages = convert_from_path(file, dpi=300)
                logging.info(f"Total de páginas convertidas: {len(pages)}")
                for i, page in enumerate(pages):
                    image_path = os.path.join(TEMP_DIR, f"page_{i + 1}.jpg")
                    page.save(image_path, "JPEG")
                    logging.info(f"Página {i + 1} salva como imagem: {image_path}")

                    try:
                        custom_config = r'--oem 3 --psm 6'
                        text = image_to_string(image_path, lang="por", config=custom_config)
                        extracted_text += text + "\n"
                        logging.info(f"Texto extraído da página {i + 1}: {text}")
                    except Exception as e:
                        logging.error(f"Erro ao executar OCR na página {i + 1}: {e}")

                    os.remove(image_path)
            except Exception as e:
                logging.error(f"Erro ao processar o PDF: {e}")
                return ""
        elif file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            logging.info("Processando imagem")
            # Processar o arquivo de imagem
            try:
                image_path = os.path.join(TEMP_DIR, f"image_to_ocr.jpg")
                img = Image.open(file)
                img.save(image_path, "JPEG")

                try:
                    custom_config = r'--oem 3 --psm 6'
                    text = image_to_string(image_path, lang="por", config=custom_config)
                    extracted_text += text + "\n"
                    logging.info(f"Texto extraído da imagem: {text}")
                except Exception as e:
                    logging.error(f"Erro ao executar OCR na imagem: {e}")

                os.remove(image_path)
            except Exception as e:
                logging.error(f"Erro ao processar a imagem: {e}")
                return ""
        else:
            logging.error(f"Tipo de arquivo não suportado: {file}")
            return ""
    except Exception as e:
        logging.error(f"Erro geral no processamento: {e}")
        return ""

    # Adicionar o texto completo ao PDF
    if extracted_text.strip():
        pdf_writer.multi_cell(0, 10, extracted_text.encode('latin-1', 'ignore').decode('latin-1'))
        logging.info(f"Texto adicionado ao PDF: {extracted_text}")
    else:
        logging.warning("Nenhum texto extraído para adicionar ao PDF.")

    # Salvar o PDF gerado
    output_path = os.path.join(DIR_PDF, output_name)
    pdf_writer.output(output_path)

    # Limpar o diretório temporário
    try:
        os.rmdir(TEMP_DIR)
    except OSError as e:
        logging.warning(f"Erro ao remover o diretório temporário: {e}")

    logging.info(f"Texto extraído com OCR e salvo no PDF: {output_path}")
    return os.path.basename(output_path)  # Retornar apenas o nome do arquivo
