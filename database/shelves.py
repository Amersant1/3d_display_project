from sqlalchemy import select
import json
from model import *


async def delete_preptype_db(
        preptype_id: int,
        session: AsyncSession = None
):
    """ Удаляет preptype по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_preptype_db(
                preptype_id = preptype_id,
                session=session
            )

    x = await session.get(PrepType, preptype_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def update_preptype_db(name: str = None, preptype_id: int = None, session: AsyncSession = None, created: datetime = None):
    """ Обновляет preptype по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_preptype_db(
                name=name,
                preptype_id=preptype_id,
                session=session,
                created=created
            )

    x = await session.get(PrepType, preptype_id)
    if name:
        x.name = name
    if created:
        x.created = created
    await session.commit()
    await session.refresh(x)

    return x


async def create_preptype_db(data: dict, session: AsyncSession=None):
    """ Создает preptype """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_preptype_db(
                data=data,
                session=session
            )

    res = PrepType(
        **data
    )
    session.add(res)

    await session.commit()
    await session.refresh(res)

    return res.id


async def get_all_shelves_db(session: AsyncSession = None):
    """ Возвращает все all_shelves из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_all_shelves_db(session)

    result = await session.execute(select(Shelf).where(Shelf.active == True).order_by(Shelf.id))

    return result.scalars().all()


async def get_preptypes_db(session: AsyncSession = None):
    """ Возвращает все preptypes из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_preptypes_db(session)

    result = await session.execute(select(PrepType).where(PrepType.active == True).order_by(PrepType.id))

    return result.scalars().all()



async def create_poultice_db(
        project_id: int,
        file: str,
        type_id: int,
        size_x: float,
        size_y: float,
        size_z: float,
        name: str,
        image: str,
        number: int,
        json_sizes_box: dict,

        number_of_shelves: int,
        width_mm: float,
        depth_mm: float,
        sides_height_mm: float,
        sides_width_mm: float,
        back_width_mm: float,
        front_width_mm: float,
        shelf_width_mm: float,
        fronton_height_mm: float,
        topper_height_mm: float,

        session: AsyncSession=None,

        session_name: str = "",
        original_id: int = 0,
        is_designed: bool = False
):
    """ Создает препак """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_poultice_db(
                project_id=project_id,
                file=file,
                type_id=type_id,
                size_x=size_x,
                size_y=size_y,
                size_z=size_z,
                name=name,
                image=image,
                number=number,
                json_sizes_box=json_sizes_box,

                number_of_shelves=number_of_shelves,
                width_mm=width_mm,
                depth_mm=depth_mm,
                sides_height_mm=sides_height_mm,
                sides_width_mm=sides_width_mm,
                back_width_mm=back_width_mm,
                front_width_mm=front_width_mm,
                shelf_width_mm=shelf_width_mm,
                fronton_height_mm=fronton_height_mm,
                topper_height_mm=topper_height_mm,

                session=session,

                session_name=session_name,
                original_id=original_id,
                is_designed=is_designed
            )

    project = await session.get(Project, project_id)
    type = await session.get(PrepType, type_id)

    if not json_sizes_box:
        res = Poultice(
            project_id=project.id,
            file=file,
            type_id=type.id,

            size_x=size_x,
            size_y=size_y,
            size_z=size_z,

            name=name,
            image=image,
            number=number,

            number_of_shelves = number_of_shelves,
            width_mm = width_mm,
            depth_mm = depth_mm,
            sides_height_mm = sides_height_mm,
            sides_width_mm = sides_width_mm,
            back_width_mm = back_width_mm,
            front_width_mm = front_width_mm,
            shelf_width_mm = shelf_width_mm,
            fronton_height_mm = fronton_height_mm,
            topper_height_mm = topper_height_mm,

            session_name=session_name,
            original_id=original_id,
            is_designed=is_designed
        )
    else:
        res = Poultice(
            project_id=project.id,
            file=file,
            type_id=type.id,

            size_x=size_x,
            size_y=size_y,
            size_z=size_z,

            name=name,
            image=image,
            number=number,

            json_sizes_box=json_sizes_box,

            number_of_shelves = number_of_shelves,
            width_mm = width_mm,
            depth_mm = depth_mm,
            sides_height_mm = sides_height_mm,
            sides_width_mm = sides_width_mm,
            back_width_mm = back_width_mm,
            front_width_mm = front_width_mm,
            shelf_width_mm = shelf_width_mm,
            fronton_height_mm = fronton_height_mm,
            topper_height_mm = topper_height_mm,

            session_name=session_name,
            original_id=original_id,
            is_designed=is_designed
        )

    session.add(res)
    await session.commit()
    await session.refresh(res)
    return res.id


async def delete_poultice_db(
        poultice_id: int,
        session: AsyncSession = None
):
    """ Удаляет poultice по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_poultice_db(
                poultice_id = poultice_id,
                session=session
            )

    x = await session.get(Poultice, poultice_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def update_poultice_db(
        poultice_id: int,
        project_id: int = None,
        file: str = None,
        type: str = None,
        size_x: float = None,
        size_y: float = None,
        size_z: float = None,
        name: str = None,
        image: str = None,
        number: int = None,
        is_designed: bool = None,
        json_sizes_box: dict = None,
        type_id:int = None,

        number_of_shelves: int = None,
        width_mm: float = None,
        depth_mm: float = None,
        sides_height_mm: float = None,
        sides_width_mm: float = None,
        back_width_mm: float = None,
        front_width_mm: float = None,
        shelf_width_mm: float = None,
        fronton_height_mm: float = None,
        topper_height_mm: float = None,

        session: AsyncSession = None,
        created: datetime = None
):
    """ Обновляет poultice по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_poultice_db(
                poultice_id = poultice_id,
                project_id = project_id,
                file = file,
                type = type,
                size_x=size_x,
                size_y=size_y,
                size_z=size_z,
                is_designed = is_designed,
                name=name,
                image=image,
                number=number,
                json_sizes_box=json_sizes_box,
                type_id=type_id,

                number_of_shelves=number_of_shelves,
                width_mm=width_mm,
                depth_mm=depth_mm,
                sides_height_mm=sides_height_mm,
                sides_width_mm=sides_width_mm,
                back_width_mm=back_width_mm,
                front_width_mm=front_width_mm,
                shelf_width_mm=shelf_width_mm,
                fronton_height_mm=fronton_height_mm,
                topper_height_mm=topper_height_mm,

                session=session,
                created=created
            )

    x = await session.get(Poultice, poultice_id)
    if project_id:
        x.project_id = project_id
    
    if file:
        x.file = file
    if type:
        x.type = type
    if size_x:
        x.size_x = size_x
    if size_y:
        x.size_y = size_y
    if size_z:
        x.size_z = size_z
    if is_designed:
        x.is_designed = is_designed
    if name:
        x.name = name
    if image:
        x.image = image
    if number:
        x.number = number
    if type_id:
        x.type_id = type_id
    if json_sizes_box:
        x.json_sizes_box = json_sizes_box

    if number_of_shelves:
        x.number_of_shelves = number_of_shelves
    if width_mm:
        x.width_mm = width_mm
    if depth_mm:
        x.depth_mm = depth_mm
    if sides_height_mm:
        x.sides_height_mm = sides_height_mm
    if sides_width_mm:
        x.sides_width_mm = sides_width_mm

    if back_width_mm:
        x.back_width_mm = back_width_mm
    if front_width_mm:
        x.front_width_mm = front_width_mm
    if shelf_width_mm:
        x.shelf_width_mm = shelf_width_mm
    if fronton_height_mm:
        x.fronton_height_mm = fronton_height_mm
    if topper_height_mm:
        x.topper_height_mm = topper_height_mm

    if created:
        x.created = created

    if project_id:
        project = await session.get(Project, project_id)
        client = await session.get(Client, project.client_id)
        project.last_updated=datetime.now()
        client.last_updated=datetime.now()
        x.last_updated=datetime.now()
    await session.commit()
    await session.refresh(x)

    return x


async def copy_poultice_in_db(session:AsyncSession = None,copy_id = None):
    # Получаем оригинальный объект Poultice по ID
    if session is None:
        async for session in make_session():
             return await copy_poultice_in_db(session,copy_id)
    result = await session.get(Poultice, copy_id)
    
    # Создаем копию объекта Poultice
    new_poultice = Poultice(
        project_id=result.project_id,
        file=result.file,
        type_id=result.type_id,
        name=result.name,
        image=result.image,
        number=result.number,
        size_x=result.size_x,
        size_y=result.size_y,
        size_z=result.size_z,
        is_designed=result.is_designed,
        created_at=datetime.now(),  # Обновляем время создания для копии
        active=result.active,
        json_sizes_box=result.json_sizes_box.copy()  # Копируем JSON-объект
    )

    # Добавляем новый объект Poultice в сессию
    session.add(new_poultice)
    await session.flush()  # Фиксируем изменения для получения нового ID

    # Получаем все связанные активные объекты Shelf
    shelves_result = await session.execute(
        select(Shelf).where(Shelf.active == True).where(Shelf.poulticle_id == copy_id)
    )

    new_shelves = []
    for shelf in shelves_result.scalars():
        # Создаем копию каждого объекта Shelf
        data = shelf.__dict__
        new_shelf = Shelf(
            shelf.__dict__       
        )
        session.add(new_shelf)
        new_shelves.append(new_shelf)
    
    # Коммитим все изменения
    await session.commit()

    # Возвращаем новые ID
    new_ids = {
        "poultice_id": new_poultice.id,
        "shelf_ids": [shelf.id for shelf in new_shelves]
    }

    return new_ids

async def get_poultices_db(session: AsyncSession=None):
    """ Возвращает все poultice из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_poultices_db(session)

    result = await session.execute(select(Poultice).where(Poultice.active == True))

    return result.scalars().all()


async def get_poultice_db(poultice_id: int, session: AsyncSession=None, session_name: str = ""):
    """ Возвращает препак по id из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_poultice_db(poultice_id=poultice_id, session=session, session_name=session_name)

    # result = await session.get(Poultice, poultice_id)
    if session_name != "":
        result = await session.execute(select(Poultice).where((Poultice.id == poultice_id) | ((Poultice.original_id == poultice_id) & (Poultice.session_name == session_name))).where(Poultice.active == True))
    else:
        result = await session.execute(select(Poultice).where(Poultice.id == poultice_id).where(Poultice.active == True))

    result = result.scalars().all()
    if len(result)==0:
        return {}
    result_orig = result[0]
    project = (await session.execute(select(Project).where(Project.id == result_orig.project_id))).all()[0][0]
    client = (await session.execute(select(Client).where(Client.id == project.client_id))).all()[0][0]
    # project = await result.project
    # client = await result.client
    # result.update({"client_name": client.name, "project_name": project.name})
    for result_iter in result:
        result_iter.client_name = client.name
        result_iter.project_name =project.name 
    return result


async def get_poultice_by_project_db(project_id: int, session: AsyncSession=None, session_name: str = ""):
    """ Возвращает все препаки по id проекта в kwargs """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_poultice_by_project_db(project_id=project_id, session=session, session_name=session_name)

    result = await session.execute(select(Poultice).where(Poultice.active == True).where(Poultice.project_id == project_id).where(Poultice.session_name == "" | Poultice.session_name == session_name))

    return result.scalars().all()


async def create_shelf_db(data: dict, session: AsyncSession = None):
    """ Создает препак """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_shelf_db(
                data=data,
                session=session
            )

    poultice = await session.get(Poultice, data["poulticle_id"])

    res = Shelf(
        **data
    )
    session.add(res)
    await session.commit()
    await session.refresh(res)
    return res.id


async def get_shelf_by_poultice_db(poultice_id: int, session: AsyncSession=None, session_name: str = ""):
    """ Возвращает все полки по id препака в kwargs """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_shelf_by_poultice_db(poultice_id=poultice_id, session=session, session_name=session_name)

    result = await session.execute(select(Shelf).where(Shelf.active == True).where(Shelf.poulticle_id == poultice_id).where((Shelf.session_name == "") | (Shelf.session_name == session_name)))

    return result.scalars().all()


async def delete_shelf_db(shelf_id: int, session: AsyncSession = None):
    """ Удаляет полку по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_shelf_db(
                shelf_id=shelf_id,
                session=session
            )

    x = await session.get(Shelf, shelf_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def update_shelf_db(
        shelf_id: int,
        width: int = None,
        length: int = None,
        heigth: int = None,
        margin_top: int = None,
        margin_bottom: int = None,
        json_shelf: str = None,
        json_rows: str = None,
        active:bool = None,
        isRows: bool = None,
        session: AsyncSession = None,
        created: datetime = None,
):
    """ Обновляет полку по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_shelf_db(
                shelf_id=shelf_id,
                width=width,
                length=length,
                heigth=heigth,
                margin_top=margin_top,
                margin_bottom=margin_bottom,
                json_shelf=json_shelf,
                json_rows=json_rows,
                active=active,
                isRows=isRows,
                session=session,
                created=created
            )

    x = await session.get(Shelf, shelf_id)
    if width:
        x.width = width
    if length:
        x.length = length
    if heigth:
        x.heigth = heigth
    if margin_top:
        x.margin_top = margin_top
    if margin_bottom:
        x.margin_bottom = margin_bottom
    if json_shelf:
        print(json_shelf)
        x.json_shelf = json_shelf
    if json_rows is not None and json_rows!=dict():
        # if not isinstance(json_rows, list):
        #     raise ValueError(f"json_rows должен быть списком, но имеет тип {type(json_rows)}")
        x.json_rows = json_rows
    if active is not None:
        x.active = active
    if isRows is not None:
        x.isRows = isRows
    if created:
        x.created = created
    poultice = await session.get(Poultice, x.poulticle_id)
    poultice.last_updated=datetime.now()
    x.last_updated=datetime.now()
    await session.commit()
    await session.refresh(x)

    return x



async def get_shelf_by_shelf_id(shelf_id: int, session: AsyncSession=None, session_name: str = ""):
    """ Возвращает все полки по id препака в kwargs """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            if session_name != "":
                result = await session.execute(select(Shelf).where((Shelf.id == shelf_id) | ((Shelf.original_id == shelf_id) & (Shelf.session_name == session_name))).where(Shelf.active == True))
            else:
                result = await session.execute(select(Shelf).where(Shelf.id == shelf_id).where(Shelf.active == True))
            return result.scalars().all()

    # result = await session.execute(select(Shelf).where(Shelf.id == shelf_id))
    #
    # return result.scalars().all()


async def get_shelf_by_session_id(shelf_id: int, session_name: str = "", session: AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            result = await session.execute(select(Shelf).where(Shelf.original_id == shelf_id).where(Shelf.session_name == session_name).where(Shelf.active == True))
            return result.scalars().all()

    result = await session.execute(select(Shelf).where(Shelf.original_id == shelf_id).where(Shelf.session_name == session_name).where(Shelf.active == True))

    return result.scalars().all()


async def get_poultice_by_session_id(poultice_id: int, session_name: str = "", session: AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            result = await session.execute(select(Poultice).where(Poultice.original_id == poultice_id).where(Poultice.session_name == session_name).where(Poultice.active == True))
            return result.scalars().all()

    result = await session.execute(select(Poultice).where(Poultice.original_id == poultice_id).where(Poultice.session_name == session_name).where(Poultice.active == True))

    return result.scalars().all()


async def get_shelf_by_session(session_name: str = "", session: AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            result = await session.execute(select(Shelf).where(Shelf.session_name == session_name).where(Shelf.active == True))
            return result.scalars().all()

    result = await session.execute(select(Shelf).where(Shelf.session_name == session_name).where(Shelf.active == True))

    return result.scalars().all()


async def get_poultice_by_session(session_name: str = "", session: AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            result = await session.execute(select(Poultice).where(Poultice.session_name == session_name).where(Poultice.active == True))
            return result.scalars().all()

    result = await session.execute(select(Poultice).where(Poultice.session_name == session_name).where(Poultice.active == True))

    return result.scalars().all()


async def get_shelves_db(session:AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_shelves_db(session)
    result = await session.execute(select(Shelf))

    return result.scalars().all()


async def check_sessions_db(poultice_id, session:AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await check_sessions_db(poultice_id, session)

    shelves = await session.execute(select(Shelf).where(Shelf.poulticle_id).where(Shelf.active == True))
    poultices = await session.execute(select(Poultice).where(Poultice.active == True).where((Poultice.id == poultice_id) | (Poultice.original_id == poultice_id)))

    return poultices.scalars().all(), shelves.scalars().all()


async def commit_session_db(session_name:str, session:AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await commit_session_db(session_name, session)

    for poultice in await get_poultice_by_session(session_name):
        if poultice.original_id == 0:
            x = await session.get(Poultice, poultice.id)
            x.session_name = ""

            await session.commit()
            await session.refresh(x)
        else:
            x = await session.get(Poultice, poultice.original_id)

            x.project_id = poultice.project_id

            x.file = poultice.file
            x.size_x = poultice.size_x
            x.size_y = poultice.size_y
            x.size_z = poultice.size_z
            x.is_designed = poultice.is_designed
            x.name = poultice.name
            x.image = poultice.image
            x.number = poultice.number
            x.type_id = poultice.type_id
            x.json_sizes_box = poultice.json_sizes_box

            x.number_of_shelves = poultice.number_of_shelves
            x.width_mm = poultice.width_mm
            x.depth_mm = poultice.depth_mm
            x.sides_height_mm = poultice.sides_height_mm
            x.sides_width_mm = poultice.sides_width_mm

            x.back_width_mm = poultice.back_width_mm
            x.front_width_mm = poultice.front_width_mm
            x.shelf_width_mm = poultice.shelf_width_mm
            x.fronton_height_mm = poultice.fronton_height_mm
            x.topper_height_mm = poultice.topper_height_mm

            x.active = poultice.active

            x.created = poultice.created
            x.last_updated = datetime.now()

            await session.commit()
            await session.refresh(x)

            x = await session.get(Poultice, poultice.id)

            x.active = False
            await session.commit()

    for shelf in await get_shelf_by_session(session_name):
        if shelf.original_id == 0:
            x = await session.get(Shelf, shelf.id)
            x.session_name = ""

            await session.commit()
            await session.refresh(x)
        else:
            x = await session.get(Shelf, shelf.original_id)

            x.width = shelf.width
            x.length = shelf.length
            x.heigth = shelf.heigth
            x.margin_top = shelf.margin_top
            x.margin_bottom = shelf.margin_bottom
            x.json_shelf = shelf.json_shelf
            x.json_rows = shelf.json_rows
            x.active = shelf.active
            x.isRows = shelf.isRows
            x.created = shelf.created
            x.last_updated = datetime.now()

            await session.commit()
            await session.refresh(x)

            x = await session.get(Shelf, shelf.id)

            x.active = False
            await session.commit()
