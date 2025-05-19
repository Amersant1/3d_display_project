from sqlalchemy import select
from datetime import datetime

from model import *


async def update_employee_db(created: datetime = None, full_name: str = None, employee_id: int = None, session: AsyncSession = None):
    """ Обновляет employee по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_employee_db(
                full_name=full_name,
                employee_id=employee_id,
                session=session,
                created=created
            )

    x = await session.get(Employee, employee_id)
    if full_name:
        x.full_name = full_name
    if created:
        x.created = created
    await session.commit()
    await session.refresh(x)

    return x


async def create_project_db(name, client_id=None, client_name=None, session = None,number=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_project_db(
                name,
                client_id=client_id,
                client_name=client_name,
                session=session
            )
    if client_id is None:
        client = Client(name=client_name)
        session.add(client)
        await session.commit()
        await session.refresh(client)
        client_id = client.id
    project = Project(name=name, client_id=client_id,number=number)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    project_id = project.id
    return project_id


async def get_projects_db(session: AsyncSession=None):
    """ Возвращает всех клиентов из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_projects_db(session)

    result = await session.execute(select(Project).where(Project.active == True).order_by(Project.id))

    return result.scalars().all()


async def get_project_db(project_id: int, session: AsyncSession=None):
    """ Возвращает проект по id из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_project_db(project_id=project_id, session=session)

    result = await session.get(Project, project_id)

    return result


async def update_project_db(project_id: int, name: str = None, client_id: int = None,number:str = None, session: AsyncSession = None, created: datetime = None):
    """ Обновляет проект по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_project_db(
                project_id=project_id,
                name=name,
                client_id=client_id,
                session=session,
                created=created,
                number=number
            )

    x = await session.get(Project, project_id)
    if name:
        x.name = name
    if client_id:
        x.client_id = client_id
    if created:
        x.created = created
    if number:
        x.number = number
    client = await session.get(Client,x.client_id)
    client.last_updated=datetime.now()
    x.last_updated=datetime.now()
    await session.commit()
    await session.refresh(x)

    return x


async def delete_project_db(project_id: int = None, session: AsyncSession = None):
    """ Удаляет project из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_project_db(
                project_id=project_id,
                session=session
            )

    x = await session.get(Project, project_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def update_client_db(created: datetime = None, name: str = None, client_id: int = None, session: AsyncSession = None):
    """ Обновляет клиента по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_client_db(
                created=created,
                name=name,
                client_id=client_id,
                session=session
            )

    x = await session.get(Client, client_id)
    if name:
        x.name = name
    if created:
        x.created = created
    await session.commit()
    await session.refresh(x)
    x.last_updated=datetime.now()
    return x


async def delete_employee_db(employee_id: int = None, session: AsyncSession = None):
    """ Удаляет employee из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_employee_db(
                employee_id=employee_id,
                session=session
            )

    x = await session.get(Employee, employee_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def delete_client_db(client_id: int = None, session: AsyncSession = None):
    """ Удаляет клиента из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_client_db(
                client_id=client_id,
                session=session
            )

    x = await session.get(Client, client_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def add_employee_db(name, session = None):
    """Получает на вход название сотрудника и возвращает id в бд"""

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await add_employee_db(name, session)
    employee = Employee(full_name=name)
    session.add(employee)
    await session.commit()
    await session.refresh(employee)
    employee_id = employee.id
    return employee_id


async def add_client_db(name, session = None):
    """Получает на вход название клиента и возвращает id в бд"""

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await add_client_db(name, session)
    client = Client(name=name)
    session.add(client)
    await session.commit()
    await session.refresh(client)
    client_id = client.id
    return client_id


async def get_clients_db(session: AsyncSession=None):
    """ Возвращает всех клиентов из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_clients_db(session)

    result = await session.execute(select(Client).where(Client.active == True).order_by(Client.id))

    return result.scalars().all()


async def get_employees_db(session: AsyncSession=None):
    """ Возвращает всех employees из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_employees_db(session)

    result = await session.execute(select(Employee).where(Employee.active == True).order_by(Employee.id))

    return result.scalars().all()
