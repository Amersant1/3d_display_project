import svgwrite
from svgpathtools import svg2paths
import numpy as np

def calculate_distance_from_center(x, y, center_x, center_y):
    """
    Вычисляет расстояние от точки до центра.

    Args:
        x (float): Координата x точки.
        y (float): Координата y точки.
        center_x (float): Координата x центра.
        center_y (float): Координата y центра.

    Returns:
        float: Расстояние от точки до центра.
    """
    return np.sqrt((x - center_x)**2 + (y - center_y)**2)

def calculate_angle(x, y, center_x, center_y):
    """
    Вычисляет угол точки относительно центра в радианах с учетом четверти.

    Args:
        x (float): Координата x точки.
        y (float): Координата y точки.
        center_x (float): Координата x центра.
        center_y (float): Координата y центра.

    Returns:
        float: Угол в радианах от 0 до 2π.
    """
    angle = np.arctan2(y - center_y, x - center_x)
    if angle < 0:
        angle += 2 * np.pi
    return angle


def svg_filter_max_distance_all_directions(input_svg, output_svg, image_size=(1000, 1000), stroke_color='black', stroke_width=2):
    """
    Фильтрует SVG-файл, оставляя только точки на максимальном расстоянии в различных направлениях.

    Args:
        input_svg (str): Путь к входному SVG-файлу.
        output_svg (str): Путь для сохранения выходного SVG-файла.
        image_size (tuple): Размер изображения (ширина, высота).
        stroke_color (str): Цвет линии контура.
        stroke_width (int): Толщина линии контура.
    """
    # Загружаем пути из SVG
    paths, _ = svg2paths(input_svg)

    # Создаем новый SVG-документ
    dwg = svgwrite.Drawing(output_svg, size=image_size, profile='tiny')

    # Определяем центр изображения
    center_x, center_y = image_size[0] / 2, image_size[1] / 2

    points_by_angle = dict()

    # Находим точки на максимальном расстоянии в каждом направлении
    for path in paths:
        for segment in path:
            if hasattr(segment, 'start') and hasattr(segment, 'end'):
                start_x, start_y = segment.start.real, segment.start.imag
                end_x, end_y = segment.end.real, segment.end.imag

                for x, y in [(start_x, start_y), (end_x, end_y)]:
                    distance = calculate_distance_from_center(x, y, center_x, center_y)
                    angle = calculate_angle(x, y, center_x, center_y)

                    # Ключ для хранения точек по углам
                    angle_key = round(angle, 5)  # округляем для уменьшения количества уникальных углов
                    distance = float(distance)
                    if angle_key not in points_by_angle:
                        points_by_angle[angle_key] = (distance, [(x, y)])
                    else:
                        max_distance, points = points_by_angle[angle_key]
                        if distance > max_distance:
                            points_by_angle[angle_key] = (distance, [(x, y)])
                        elif distance == max_distance:
                            points_by_angle[angle_key][1].append((x, y))

    # Создаем контуры только с точками на максимальном расстоянии для всех направлений
    for angle_key, (max_distance, points) in points_by_angle.items():
        for x, y in points:
            dwg.add(dwg.circle(center=(x, y), r=stroke_width, stroke=stroke_color, fill='none'))

    # Сохраняем новый SVG-файл
    dwg.save()

svg_file = "media\V22_09_21_Rexona_Аэрозоль_150ml_Нежно_и_сочно__top.svg"
output_file = "output_optimized.svg"
# Создаем изображение
image = svg_filter_max_distance_all_directions(svg_file,output_file,)

# Сохраняем изображение
image.save("output_image.png")

# Показываем изображение
image.show()