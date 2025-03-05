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


async def update_preptype_db(name: str = None, preptype_id: int = None, session: AsyncSession = None):
    """ Обновляет preptype по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_preptype_db(
                name=name,
                preptype_id=preptype_id,
                session=session
            )

    x = await session.get(PrepType, preptype_id)
    if name:
        x.name = name
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
        session: AsyncSession=None
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
                session=session
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
            number=number
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

            json_sizes_box=json_sizes_box
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
        session: AsyncSession = None
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
                session=session,
            )

    x = await session.get(Poultice, poultice_id)
    if project_id:
        x.width = project_id
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
    await session.commit()
    await session.refresh(x)

    return x


async def get_poultices_db(session: AsyncSession=None):
    """ Возвращает все poultice из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_poultices_db(session)

    result = await session.execute(select(Poultice).where(Poultice.active == True))

    return result.scalars().all()


async def get_poultice_db(poultice_id: int, session: AsyncSession=None):
    """ Возвращает препак по id из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_poultice_db(poultice_id=poultice_id, session=session)

    result = await session.get(Poultice, poultice_id)

    return result


async def get_poultice_by_project_db(project_id: int, session: AsyncSession=None):
    """ Возвращает все препаки по id проекта в kwargs """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_poultice_by_project_db(project_id=project_id, session=session)

    result = await session.execute(select(Poultice).where(Poultice.active == True).where(Poultice.project_id == project_id))

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


async def get_shelf_by_poultice_db(poultice_id: int, session: AsyncSession=None):
    """ Возвращает все полки по id препака в kwargs """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_shelf_by_poultice_db(poultice_id=poultice_id, session=session)

    result = await session.execute(select(Shelf).where(Shelf.active == True).where(Shelf.poulticle_id == poultice_id))

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
        session: AsyncSession = None
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
                session=session
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
    if json_rows:
        if not isinstance(json_rows, list):
            raise ValueError(f"json_rows должен быть списком, но имеет тип {type(json_rows)}")
        x.json_rows = json_rows
    await session.commit()
    await session.refresh(x)

    return x



async def get_shelf_by_shelf_id(shelf_id: int, session: AsyncSession=None):
    """ Возвращает все полки по id препака в kwargs """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            result = await session.execute(select(Shelf).where(Shelf.id == shelf_id))
            return result.scalars().all()

    result = await session.execute(select(Shelf).where(Shelf.id == shelf_id))

    return result.scalars().all()


async def get_shelves_db(session:AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_shelves_db(session)
    result = await session.execute(select(Shelf))

    return result.scalars().all()