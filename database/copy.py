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
    if hasattr(clone,'created_at'):
        clone.created_at = datetime.now()
    if hasattr(clone,'created'):
        clone.created = datetime.now()
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
    # y.created_at = datetime.now()

    res = [{"type": "client", "id": y.id, "old_id": x.id}]
    for el in (await session.execute(select(Project).where(Project.client_id == x.id))).scalars().all():
        z = await clone_project_db(el.id, client_id=y.id, parent_id=y.id, parent_type="client", old_parent_id=x.id)
        res += z
    for el in (await session.execute(select(Product).where(Product.client_id == x.id))).scalars().all():
        z = await clone_product_db(el.id, parent_id=y.id, parent_type="client", client_id=y.id, old_parent_id=x.id)
        res += z

    return res


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

    res = [{"type": "employee", "id": y.id, "old_id": x.id}]
    for el in (await session.execute(select(Project).where(Project.employee_id == x.id))).scalars().all():
        z = await clone_project_db(el.id, employee_id=y.id, parent_id=y.id, parent_type="employee", old_parent_id=x.id)
        res += z

    return res


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

    res = [{"type": "packaging_type", "id": y.id, "old_id": x.id}]
    for el in (await session.execute(select(Product).where(Product.packaging_type_id == x.id))).scalars().all():
        z = await clone_product_db(
            el.id, parent_id=y.id,
            parent_type="packaging_type",
            packaging_type_id=y.id,
            old_parent_id=x.id
        )
        res += z

    return res


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

    res = [{"type": "prep_type", "id": y.id, "old_id": x.id}]
    for el in (await session.execute(select(Poultice).where(Poultice.type_id == x.id))).scalars().all():
        z = await clone_poultice_db(el.id, type_id=y.id, parent_id=y.id, parent_type="prep_type", old_parent_id=x.id)
        res += z

    return res


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

    res = [{"type": "product_category", "id": y.id, "old_id": x.id}]
    for el in (await session.execute(select(Product).where(Product.category_id == x.id))).scalars().all():
        z = await clone_product_db(
            el.id, parent_id=y.id,
            parent_type="product_category",
            category_id=y.id, old_parent_id=x.id
        )
        res += z

    return res


async def clone_project_db(
        instance_id: int,
        client_id: int = None,
        employee_id: int = None,
        session: AsyncSession = None,
        parent_id: int = None,
        parent_type: str = None,
        old_parent_id: int = None
):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_project_db(
                instance_id=instance_id,
                client_id=client_id,
                employee_id=employee_id,
                parent_id=parent_id,
                parent_type=parent_type,
                old_parent_id=old_parent_id,
                session=session
            )

    x = await session.get(Project, instance_id)

    if client_id:
        y = await _clone_model(model=x, client_id=client_id)
    elif employee_id:
        y = await _clone_model(model=x, employee_id=client_id)
    else:
        y = await _clone_model(model=x)

    if not (parent_id and parent_type and old_parent_id):
        res = [{"type": "project", "id": y.id, "old_id": x.id}]
    else:
        res = [{
            "type": "project",
            "id": y.id,
            "old_id": x.id,
            "parent_type": parent_type,
            "parent_id": parent_id,
            "old_parent_id": old_parent_id
        }]

    for el in (await session.execute(select(Poultice).where(Poultice.project_id == x.id))).scalars().all():
        z = await clone_poultice_db(el.id, project_id=y.id, parent_id=y.id, parent_type="project", old_parent_id=x.id)
        res += z

    return res


async def clone_poultice_db(
        instance_id: int,
        project_id: int = None,
        type_id: int = None,
        session: AsyncSession = None,
        parent_id: int = None,
        parent_type: str = None,
        old_parent_id: int = None
):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_poultice_db(
                instance_id=instance_id,
                project_id=project_id,
                type_id=type_id,
                parent_id=parent_id,
                parent_type=parent_type,
                old_parent_id=old_parent_id,
                session=session
            )

    x = await session.get(Poultice, instance_id)

    if project_id:
        y = await _clone_model(model=x, project_id=project_id)
    elif type_id:
        y = await _clone_model(model=x, type_id=type_id)
    else:
        y = await _clone_model(model=x)

    if not (parent_id and parent_type and old_parent_id):
        res = [{"type": "poultice", "id": y.id, "old_id": x.id}]
    else:
        res = [{
            "type": "poultice",
            "id": y.id,
            "old_id": x.id,
            "parent_type": parent_type,
            "parent_id": parent_id,
            "old_parent_id": old_parent_id
        }]

    for el in (await session.execute(select(Shelf).where(Shelf.poulticle_id == x.id))).scalars().all():
        z = await clone_shelf_db(el.id, parent_id=y.id, parent_type="poultice", poulticle_id=y.id, old_parent_id=x.id)
        res += z

    return res


async def clone_shelf_db(
        instance_id: int,
        session: AsyncSession = None,
        parent_id: int = None,
        parent_type: str = None,
        old_parent_id: int = None,
        poulticle_id: int = None
):

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_shelf_db(
                instance_id=instance_id,
                parent_id=parent_id,
                parent_type=parent_type,
                old_parent_id=old_parent_id,
                poulticle_id=poulticle_id,
                session=session
            )

    x = await session.get(Shelf, instance_id)

    if poulticle_id:
        y = await _clone_model(model=x, poulticle_id=poulticle_id)
    else:
        y = await _clone_model(model=x)

    if not (parent_id and parent_type and old_parent_id):
        return [{"type": "shelf", "id": y.id, "old_id": x.id}]
    else:
        return [{
            "type": "shelf",
            "id": y.id,
            "old_id": x.id,
            "parent_type": parent_type,
            "parent_id": parent_id,
            "old_parent_id": old_parent_id
        }]


async def clone_product_db(
        instance_id: int,
        session: AsyncSession = None,
        parent_id: int = None,
        parent_type: str = None,
        old_parent_id: int = None,
        category_id: int = None,
        packaging_type_id: int = None,
        client_id: int = None
):

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await clone_product_db(
                instance_id=instance_id,
                parent_id=parent_id,
                parent_type=parent_type,
                old_parent_id=old_parent_id,
                category_id=category_id,
                packaging_type_id=packaging_type_id,
                client_id=client_id,
                session=session
            )

    x = await session.get(Product, instance_id)

    if category_id:
        y = await _clone_model(model=x, category_id=category_id)
    elif packaging_type_id:
        y = await _clone_model(model=x, packaging_type_id=packaging_type_id)
    elif client_id:
        y = await _clone_model(model=x, client_id=client_id)
    else:
        y = await _clone_model(model=x)

    if not (parent_id and parent_type and old_parent_id):
        return [{"type": "product", "id": y.id, "old_id": x.id}]
    else:
        return [{
            "type": "product",
            "id": y.id,
            "old_id": x.id,
            "parent_type": parent_type,
            "parent_id": parent_id,
            "old_parent_id": old_parent_id,
        }]
