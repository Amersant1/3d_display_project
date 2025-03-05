from sqlalchemy import select

from model import *


async def _clone_model(model, session: AsyncSession = None, **kwargs):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await _clone_model(
                model=model,
                session=session,
                **kwargs
            )

    """Clone an arbitrary sqlalchemy model object without its primary key values."""
    # Ensure the model’s data is loaded before copying.
    model.id

    table = model.__table__
    non_pk_columns = [k for k in table.columns.keys() if k not in table.primary_key.columns.keys()]
    data = {c: getattr(model, c) for c in non_pk_columns}
    data.update(kwargs)

    clone = model.__class__(**data)
    session.add(clone)
    await session.commit()
    return clone


async def clone_client_db(instance_id: int, session: AsyncSession = None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_client_db(
                instance_id=instance_id,
                session=session
            )

    x = await session.get(Client, instance_id)

    y = await _clone_model(model=x)

    for el in (await session.execute(select(Project).where(Project.client_id == x.id))).scalars().all():
        await clone_project_db(el.id, client_id=y.id)
        # await _clone_model(el, client_id=y.id)
    for el in (await session.execute(select(Product).where(Product.client_id == x.id))).scalars().all():
        await _clone_model(el, client_id=y.id)

    return y.id


async def clone_employee_db(instance_id: int, session: AsyncSession = None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_employee_db(
                instance_id=instance_id,
                session=session
            )

    x = await session.get(Employee, instance_id)

    y = await _clone_model(model=x)

    for el in (await session.execute(select(Project).where(Project.employee_id == x.id))).scalars().all():
        await clone_project_db(el.id, employee_id=y.id)
        # await _clone_model(el, employee_id=y.id)

    return y.id


async def clone_packaging_type_db(instance_id: int, session: AsyncSession = None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_packaging_type_db(
                instance_id=instance_id,
                session=session
            )

    x = await session.get(PackagingType, instance_id)

    y = await _clone_model(model=x)

    for el in (await session.execute(select(Product).where(Product.packaging_type_id == x.id))).scalars().all():
        await _clone_model(el, packaging_type_id=y.id)

    return y.id


async def clone_prep_type_db(instance_id: int, session: AsyncSession = None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_prep_type_db(
                instance_id=instance_id,
                session=session
            )

    x = await session.get(PrepType, instance_id)

    y = await _clone_model(model=x)

    for el in (await session.execute(select(Poultice).where(Poultice.type_id == x.id))).scalars().all():
        # await _clone_model(el, type_id=y.id)
        await clone_poultice_db(el.id, type_id=y.id)

    return y.id


async def clone_product_category_db(instance_id: int, session: AsyncSession = None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_product_category_db(
                instance_id=instance_id,
                session=session
            )

    x = await session.get(ProductCategory, instance_id)

    y = await _clone_model(model=x)

    for el in (await session.execute(select(Product).where(Product.category_id == x.id))).scalars().all():
        await _clone_model(el, category_id=y.id)

    return y.id


async def clone_project_db(instance_id: int, client_id: int = None, employee_id: int = None, session: AsyncSession = None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_project_db(
                instance_id=instance_id,
                client_id=client_id,
                employee_id=employee_id,
                session=session
            )

    x = await session.get(Project, instance_id)

    if client_id:
        y = await _clone_model(model=x, client_id=client_id)
    elif employee_id:
        y = await _clone_model(model=x, employee_id=client_id)
    else:
        y = await _clone_model(model=x)

    for el in (await session.execute(select(Poultice).where(Poultice.project_id == x.id))).scalars().all():
        # await _clone_model(el, project_id=y.id)
        await clone_poultice_db(el.id, project_id=y.id)

    return y.id


async def clone_poultice_db(instance_id: int, project_id: int = None, type_id: int = None, session: AsyncSession = None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_poultice_db(
                instance_id=instance_id,
                project_id=project_id,
                type_id=type_id,
                session=session
            )

    x = await session.get(Poultice, instance_id)

    if project_id:
        y = await _clone_model(model=x, project_id=project_id)
    elif type_id:
        y = await _clone_model(model=x, type_id=type_id)
    else:
        y = await _clone_model(model=x)

    for el in (await session.execute(select(Shelf).where(Shelf.poulticle_id == x.id))).scalars().all():
        await _clone_model(el, poulticle_id=y.id)

    return y.id


async def clone_shelf_db(instance_id: int, session: AsyncSession = None):
    """ Final cloning step """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_shelf_db(
                instance_id=instance_id,
                session=session
            )

    x = await session.get(Shelf, instance_id)

    y = await _clone_model(model=x)
    return y.id


async def clone_product_db(instance_id: int, session: AsyncSession = None):
    """ Final cloning step """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_product_db(
                instance_id=instance_id,
                session=session
            )

    x = await session.get(Product, instance_id)

    y = await _clone_model(model=x)
    return y.id
