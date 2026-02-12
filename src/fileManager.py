import fitz
from pathlib import Path
from PIL import Image
import os

class FileManager:
    def __init__(self, tmp_path):
        self.tmp_path = tmp_path
        pass

    def convertor_pdf_to_png(self, pdf_file_path):
        ### Получаем путь к PDF файл > pdf_file_path
        ### Откроем PDF файл
        # Нужно поставить проверку !!!
        pdf_doc = fitz.open(pdf_file_path)
        # Называние файл изображение
        file_names = []
        ### Проходим по каждой странице
        for page_index in range(len(pdf_doc)):
            ### Загружаем страницу
            page = pdf_doc.load_page(page_index)  
            ### Рендерим страницу в изображение (pixmap)
            ### matrix помогает улучшить качество (масштабирование)
            ### Увеличиваем разрешение в 2 раза (для четкости)
            zoom = 2  
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            ### Сохраняем файл
            file_name_pdf = os.path.basename(pdf_file_path)
            file_name = f"{file_name_pdf}_{page_index + 1}.png"
            output_filename = f"{self.tmp_path}/{file_name}"
            pix.save(output_filename)
            file_names.append(file_name)
        pdf_doc.close()
        return file_names
    
    
    def compress_image(self, input_path, output_path, target_size_mb=10):
        img = Image.open(input_path)
        quality = 95  # Начинаем с высокого качества
        
        while True:
            # Сохраняем во временный файл для проверки веса
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            
            # Проверяем размер файла в байтах
            if os.path.getsize(output_path) <= target_size_mb * 1024 * 1024 or quality <= 10:
                break
            
            quality -= 5
        
        return True
    
    def delete_file(self, file_path):
        del_file = Path(file_path)
        del_file.unlink()
