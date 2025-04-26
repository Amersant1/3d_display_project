import trimesh
import svgwrite
import math

"""НУЖНО ЧИТАТЬ МИНИМАЛЬНЫЕ ЗНАЧЕНИЯ ПРОЕКЦИИ ЗА НОЛЬ"""

import math

def determine_quadrant(center_x, center_y, new_point):
    # Извлечение координат точки
    x, y = new_point[0], new_point[1]
    
    # Определение четверти
    if x > center_x and y > center_y:
        quadrant = 1
    elif x < center_x and y > center_y:
        quadrant = 2
    elif x < center_x and y < center_y:
        quadrant = 3
    elif x > center_x and y < center_y:
        quadrant = 4
    else:
        # Точка на одной из осей или в центре
        quadrant = None

    # Вычисление расстояния до центра
    distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    return quadrant, round(distance, 2)  # Округляем расстояние до 2 знаков после запятой


def convert_from_obj_to_svg(path, filename: str, directory: str = ""):
# Загрузка .obj файла
    mesh = trimesh.load(path)
    print(f"Количество вершин: {len(mesh.vertices)}")
    print(f"Количество граней: {len(mesh.faces)}")

    # Вывод координат первых нескольких вершин для проверки
    print("Первые несколько вершин:")
    for i in range(5):
        print(mesh.vertices[i])
    # Устанавливаем видовые углы для проекций
    views = {
        'front': [0, 0, 1],   # Вид спереди
        'side': [1, 0, 0],    # Вид сбоку
        'top': [0, 1, 0]      # Вид сверху
    }
    x_min,y_min,z_min = 1000000,1000000,1000000
    suma_x,suma_y,suma_z=0,0,0
    length = len(mesh.vertices)
    for verticle in mesh.vertices:
        suma_x += verticle[0]
        suma_y += verticle[1]
        suma_z += verticle[2]
        if verticle[0]<x_min:
            x_min = verticle[0]
        if verticle[1]<y_min:
            y_min = verticle[1]
        if verticle[2]<z_min:
            z_min = verticle[2]
    center_x = suma_x/length
    center_y = suma_y/length
    center_z = suma_z/length
    



    # Функция для генерации SVG из 2D проекции
    def generate_svg(entities, filename):
        dwg = svgwrite.Drawing(filename)
        for entity in entities:
            if isinstance(entity, trimesh.path.entities.Line):
                # Получение координат начала и конца линии
                # points = [(point[0], point[1]) for point in entity.nodes]
                # points = [(float(point[0]), float(point[1])) for point in entity.nodes]
                # Получение координат начала и конца линии
                start_point = mesh.vertices[entity.points[0]]
                end_point = mesh.vertices[entity.points[1]]
                points = [(start_point[0], start_point[1]), (end_point[0], end_point[1])]
                dwg.add(dwg.polyline(points, stroke='black', fill='none'))
            elif isinstance(entity, trimesh.path.entities.Arc):
                # Дискретизация дуги
                points = [(point[0], point[1]) for point in entity.discrete(20)]
                dwg.add(dwg.polyline(points, stroke='black', fill='none'))
        dwg.save()

    def make_projection(points,direction):
        angles_points  = {1:dict(), 2:dict(), 3:dict(), 4:dict()}
        #тут мы храним четверти окружности вокруг центра, а внутри них угол наклона, а внутри него точку и расстояние от центра
        new_points = []
        for point in points:
            new_point = []
            for i in range(len(direction)):
                if direction[i] !=1:
                    new_point.append( float(point[i]))
            if direction[0]==1:
                angle =( new_point[0]-center_y)/(new_point[1]-center_z)
                quadrant,distance = determine_quadrant(center_y,center_z,new_point)
            elif direction[1]==1:
                
                angle = (new_point[0]-center_x) / (new_point[1]-center_z)
                quadrant,distance = determine_quadrant(center_x,center_z,new_point)
            elif direction[2]==1: 
                angle = (new_point[0]-center_x) / (new_point[1]-center_y)
                quadrant,distance = determine_quadrant(center_x,center_y,new_point)
            
            angle = round(angle, 2)
            if angle in angles_points[quadrant]:
                last_distance= angles_points[quadrant][angle][1]
                if last_distance < distance: 
                    angles_points[quadrant][angle] = (new_point, distance)
            else:
                angles_points[quadrant][angle] = (new_point, distance)

            # new_points.append(new_point)
        new_points = list()

        for quadrant in angles_points:
            for point_key in angles_points[quadrant]:
                point=angles_points[quadrant][point_key]
                new_points.append(point[0])

        
        return new_points


    def change_0_coordinates(point):
        point[0] = point[0]-x_min
        point[1] = point[1]-y_min
        point[2] = point[2]-z_min

    def generate_svg2(direction, filename):
        points=list()
        dwg = svgwrite.Drawing(filename)
        change_0_coordinates(mesh.vertices[0])
        for i in range(1,len(mesh.vertices)):
            change_0_coordinates(mesh.vertices[i])
            # point = mesh.vertices[i-1],mesh.vertices[i]
            points.append(list(mesh.vertices[i-1]))
        points = make_projection(points,direction)
# Дискретизация дуги
        dwg.add(dwg.polyline(points, stroke='black', fill='none'))
        dwg.save()
    # Генерация и сохранение проекций

    def generate_svg_from_points(direction, filename):
        points=list()
        dwg = svgwrite.Drawing(filename)
        change_0_coordinates(mesh.vertices[0])
        for i in range(1,len(mesh.vertices)):
            change_0_coordinates(mesh.vertices[i])
            # point = mesh.vertices[i-1],mesh.vertices[i]
            points.append(list(mesh.vertices[i-1]))
        points = make_projection(points,direction)
        svg_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
        svg_header += '<svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">\n'
        svg_footer = '</svg>'
        
        lines = []
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            lines.append(f'  <line x1="{start_point[0]}" y1="{start_point[1]}" x2="{end_point[0]}" y2="{end_point[1]}" stroke="black" stroke-width="1" />\n')

        # Добавляем точки
        points_str = ''
        for (x, y) in points:
            points_str += f'  <circle cx="{x}" cy="{y}" r="1" fill="black" />\n'

        svg_content = svg_header + ''.join(lines) + points_str + svg_footer

        with open(filename, 'w') as file:
            file.write(svg_content)
    # new_points = [(10, 20), (30, 40), (50, 60), (70, 80), (90, 100)]
    # generate_svg_from_points(new_points, 'points_lines.svg')
    for view_name, direction in views.items():
            # Проекция
        # section = mesh.section(plane_origin=[0, 0, 0], plane_normal=direction)
        # if section:
        #     # Получение 2D представления проекции
        #     projection, _ = section.to_planar()

        #     # Экспорт в SVG
        #     # generate_svg(projection.entities, f'{view_name}.svg')
        
        generate_svg_from_points(direction, f'{directory}/{filename}_{view_name}.svg')


    print("Проекции сохранены как SVG файлы.")




def distance(p1, p2):
    """Возвращает расстояние между двумя точками."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def nearest_points(points, start_index):
    """Возвращает индекс ближайшей точки к указанной точке."""
    distances = [(i, distance(points[start_index], points[i])) for i in range(len(points)) if i != start_index]
    return min(distances, key=lambda x: x[1])[0]



# convert_from_obj_to_svg("media\Full LARB 15WL RUS.obj","out_mycode","D:/ZAVOD")