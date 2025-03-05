import trimesh
import svgwrite

"""НУЖНО ЧИТАТЬ МИНИМАЛЬНЫЕ ЗНАЧЕНИЯ ПРОЕКЦИИ ЗА НОЛЬ"""



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
    for verticle in mesh.vertices:
        if verticle[0]<x_min:
            x_min = verticle[0]
        if verticle[1]<y_min:
            y_min = verticle[1]
        if verticle[2]<z_min:
            z_min = verticle[2]


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
        new_points = []
        for point in points:
            new_point = []
            for i in range(len(direction)):
                if direction[i] !=1:
                    new_point.append( float(point[i]))
            new_points.append(new_point)
        return new_points


    def change_0_coordinates(point):
        point[0] = point[0]-x_min
        point[1] = point[1]-y_min
        point[2] = point[2]-z_min

    def generate_svg2(direction, filename):
        dwg = svgwrite.Drawing(filename)
        change_0_coordinates(mesh.vertices[0])
        for i in range(1,len(mesh.vertices)):
            change_0_coordinates(mesh.vertices[i])
            points = mesh.vertices[i-1],mesh.vertices[i]
            points = make_projection(points,direction)
    # Дискретизация дуги
            dwg.add(dwg.polyline(points, stroke='black', fill='none'))
        dwg.save()
    # Генерация и сохранение проекций
    for view_name, direction in views.items():
        # Проекция
        # section = mesh.section(plane_origin=[0, 0, 0], plane_normal=direction)
        # if section:
        #     # Получение 2D представления проекции
        #     projection, _ = section.to_planar()

        #     # Экспорт в SVG
        #     # generate_svg(projection.entities, f'{view_name}.svg')
        
        generate_svg2(direction, f'{directory}/{filename}_{view_name}.svg')

    print("Проекции сохранены как SVG файлы.")



