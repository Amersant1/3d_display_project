from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image
import io
import tempfile
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

shelf_width_mm = 200  # ширина строки с полкой
shelf_height_mm = 40  # высота строки с полкой
image_spacing_mm = 5  # расстояние между изображениями на одной строке
full_image_height_mm = 153  # высота большого изображения слева
full_image_width_mm = 75 # ширина большого изображения слева
margin_image_height_mm = 40 # Высота большого изображение слева над началом координат
width_till_shelf_mm = 86 #Расстояние до первого изображения на полке
wisth_shelf_mm = 40 #ширина изображения полки

background_color = (200, 200, 200)  # Серый цвет (RGB)
text_color = (0, 0, 255)  # Синий цвет (RGB)

dpi = 72  # Изменено: 72 dpi для соответствия размерам в миллиметрах

from_mm_to_px = lambda x: int(x* mm_to_inch * dpi)

mm_to_inch = 1 / 25.4
shelf_width_px = from_mm_to_px(shelf_width_mm)
shelf_height_px = from_mm_to_px(shelf_height_mm)
margin_image_height_mm = from_mm_to_px(margin_image_height_mm)
image_spacing_px = from_mm_to_px(image_spacing_mm)
full_image_height_px = from_mm_to_px(full_image_height_mm)
full_image_width_px = from_mm_to_px(full_image_width_mm)
width_till_shelf_px = from_mm_to_px(width_till_shelf_mm)
width_shelf_px = from_mm_to_px(wisth_shelf_mm)


def draw_centered_text(c, width, height, header_text):
    """Рисует текст по центру заданной ширины."""
    text_width = stringWidth(header_text, "Times-Roman", 14)  # Используйте шрифт и размер, как в вашем коде
    x = (width - text_width) / 2
    c.setFillColor(colors.blue)
    c.drawString(x, height - 20, header_text)


def generate_plannogram(data, output_path='plannogram.pdf'):
    """Генерирует планограмму в PDF-файл на основе предоставленных данных."""
    pdfmetrics.registerFont(TTFont('Times-Roman', 'fonts/timesnewromanpsmt.ttf')) # Измените путь, если файл шрифта находится в другом месте

    c = canvas.Canvas(output_path, pagesize=(A4[1], A4[0]),background_color=background_color,encoding='utf-8')  # Изменено: A4, повернутый на 90 градусов
    width, height = A4[1], A4[0]  # Изменено: A4, повернутый на 90 градусов
    c.setFont('Times-Roman', 8)  # Устанавливаем шрифт Helvetica-Bold для item_text

    # Загружаем большое изображение слева
    left_img = Image.open(data['left_image'])
    left_img = left_img.resize((int(width * 0.4), int(height * 0.8)))
    img_buffer = io.BytesIO()
    left_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
        tmp_img.write(img_buffer.read())
        tmp_img_path = tmp_img.name

    c.drawImage(tmp_img_path, 0, margin_image_height_mm, width=full_image_width_px, height=full_image_height_px)

    # Удаляем временный файл
    os.unlink(tmp_img_path)

    # Рисуем шапку
    header_text = f"№ {data['header']['client_name']} - {data['header']['project_name']} - {data['header']['poultice_name']}"
    c.setFillColor(colors.blue)
    c.setFont('Times-Roman', 14)  # Устанавливаем шрифт Helvetica-Bold для item_text

    draw_centered_text(c,width,height,header_text)
    c.setFont('Times-Roman', 8)  # Устанавливаем шрифт Helvetica-Bold для item_text

    # Рисуем подвал
    footer_text = f"Размер препака: {data['footer']['pack_size']}"
    c.drawString(50, 100, footer_text)
    footer_text = f"Размер короба: {data['footer']['pack_in_box']}"
    c.drawString(50,90,footer_text)
    # Рисуем полки и описания
    for i, shelf in enumerate(data['shelf_data']):
        y = full_image_height_px - (i) * shelf_height_px  + shelf_height_px
        x = width_till_shelf_px
        for j, img_path in enumerate(shelf['images']):
            pict_height = int(shelf_height_px *0.8)
            shelf_img = Image.open(img_path)
            y_pict = y - pict_height
            shelf_img = shelf_img.resize((width_shelf_px, pict_height))
            img_buffer = io.BytesIO()
            shelf_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_img:
                tmp_img.write(img_buffer.read())
                tmp_img_path = tmp_img.name

            c.drawImage(tmp_img_path, x,y_pict, width=shelf_img.width, height=shelf_img.height)
            os.unlink(tmp_img_path)

            x += int(width_shelf_px) + image_spacing_px

        # Рисуем список товаров
        text_x = x
        text_y = y - 5
        for item in shelf['description']:
            item_text = f"{item['name']}"
            item_count = f"({item['quantity']})"
            item_text_width = c.stringWidth(item_text, 'Times-Roman', 12)  # Ширина текста item_text
            item_count_x = width - c.stringWidth(item_count, 'Times-Roman', 8) - 50  # Расчет x для item_count
            c.setFont('Times-Roman', 6)  # Устанавливаем шрифт Helvetica-Bold для item_text
            c.drawString(text_x, text_y, item_text)
            c.setFont('Times-Roman', 6)  # Уменьшаем шрифт для item_count
            c.drawString(item_count_x, text_y, item_count)
            c.setFont('Times-Roman', 6)  # Восстанавливаем шрифт для следующего item_text
            text_y -= 10

    c.save()

data = {
    'header': {
        'client_name': 'Юниливер',
        'project_name': 'Препак ЛАБ Бьюти 5ка апр - май 2025',
        'poultice_name': 'Препак 1',
        'date': '29 января 2025г'
    },
    'left_image': 'media/front/total_front.jpg',
    'shelf_data': [
        {
            'images': ['media/front/shelf1_front.jpg', 'media/front/shelf1_top.jpg'],
            'description': [
                {'name': 'ФА Роликовый антиперспирант', 'quantity': '50 мл'},
                {'name': 'ФА MEN Роликовый антиперспирант', 'quantity': '50 мл'},
                # ... другие товары для полки 1
            ]
        },
        {
            'images': ['media/front/shelf2_front.jpg', 'media/front/shelf2_top.jpg'],
            'description': [
                {'name': 'TESTTEST TEST', 'quantity': '150 мл'},
                {'name': 'СУПЕРДОЛГОЕ СУПЕРДОЛГОЕ ОЧЕНЬ СУПЕР ДОЛГОЕ НАЗВАНИЕ', 'quantity': '150 мл'},
                # ... другие товары для полки 2
            ]
        },
        {
            'images': ['media/front/shelf1_front.jpg', 'media/front/shelf1_top.jpg'],
            'description': [
                {'name': 'ФА Роликовый антиперспирант', 'quantity': '50 мл'},
                {'name': 'ФА MEN Роликовый антиперспирант', 'quantity': '50 мл'},
                # ... другие товары для полки 1
            ]
        },
        {
            'images': ['media/front/shelf1_front.jpg', 'media/front/shelf1_top.jpg'],
            'description': [
                {'name': 'ФА Роликовый антиперспирант', 'quantity': '50 мл'},
                {'name': 'ФА MEN Роликовый антиперспирант', 'quantity': '50 мл'},
                # ... другие товары для полки 1
            ]
        },
        # ... данные для остальных полок
    ],
    'footer': {
        'pack_size': '575x375',
        'pack_in_box': '50x300x1300'
    }
}
# Пример использования
generate_plannogram(data, 'plannogram.pdf')