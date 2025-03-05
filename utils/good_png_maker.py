from PIL import Image

def change_black_to_transparent(image_path, output_path):
    # Открываем изображение и конвертируем его в формат RGBA
    image = Image.open(image_path).convert("RGBA")
    
    # Получаем данные изображения
    datas = image.getdata()
    
    new_data = []
    for item in datas:
        # Черный цвет (0, 0, 0)
        if item[:3] == (0, 0, 0):
            # Заменяем на прозрачный (0, 0, 0, 0)
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    
    # Обновляем данные изображения
    image.putdata(new_data)
    
    # Сохраняем новое изображение в формате PNG
    image.save(output_path, "PNG")

if __name__== "__main__":
    change_black_to_transparent('media/bottls.jpg', 'output.png')


