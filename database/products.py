from sqlalchemy import select

from model import *


async def create_packagingtype_db(data: dict, session: AsyncSession=None):
    """ Создает packagingtype """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_packagingtype_db(
                data=data,
                session=session
            )

    res = PackagingType(
        **data
    )
    session.add(res)

    await session.commit()
    await session.refresh(res)

    return res.id


async def update_packagingtype_db(
        name: str = None,
        front_svg: str = None,
        side_svg: str = None,
        top_svg: str = None,
        packagingtype_id: int = None,
        object: str = None,
        session: AsyncSession = None
):
    """ Обновляет packagingtype по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_packagingtype_db(
                name=name,
                front_svg=front_svg,
                side_svg=side_svg,
                top_svg=top_svg,
                packagingtype_id=packagingtype_id,
                object=object,
                session=session
            )

    x = await session.get(PackagingType, packagingtype_id)
    if name:
        x.name = name
    if front_svg:
        x.front_svg = front_svg
    if side_svg:
        x.side_svg = side_svg
    if top_svg:
        x.top_svg = top_svg
    if object:
        x.object = object
    await session.commit()
    await session.refresh(x)

    return x


async def delete_packagingtype_db(packagingtype_id: int = None, session: AsyncSession = None):
    """ Удаляет packagingtype из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_packagingtype_db(
                packagingtype_id=packagingtype_id,
                session=session
            )

    x = await session.get(PackagingType, packagingtype_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def create_productcategory_db(name, session = None):
    """Получает на вход название productcategory и возвращает id в бд"""

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_productcategory_db(name, session)
    productcategory = ProductCategory(name=name)
    session.add(productcategory)
    await session.commit()
    await session.refresh(productcategory)
    productcategory_id = productcategory.id
    return productcategory_id


async def update_productcategory_db(name: str = None, productcategory_id: int = None, session: AsyncSession = None):
    """ Обновляет клиента по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_productcategory_db(
                name=name,
                productcategory_id=productcategory_id,
                session=session
            )

    x = await session.get(ProductCategory, productcategory_id)
    if name:
        x.name = name
    await session.commit()
    await session.refresh(x)

    return x


async def delete_productcategory_db(productcategory_id: int = None, session: AsyncSession = None):
    """ Удаляет productcategory из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_productcategory_db(
                productcategory_id=productcategory_id,
                session=session
            )

    x = await session.get(ProductCategory, productcategory_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def create_product_db(data: dict, session: AsyncSession=None):
    """ Создает product """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_product_db(
                data=data,
                session=session
            )

    client = await session.get(Client, data["client_id"])
    category = await session.get(ProductCategory, data["category_id"])
    pack_type = await session.get(Client, data["packaging_type_id"])

    res = Product(
        **data
    )
    session.add(res)

    await session.commit()
    await session.refresh(res)

    return res.id


async def delete_product_db(
        product_id: int,
        session: AsyncSession = None
):
    """ Удаляет product по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_product_db(
                product_id=product_id,
                session=session,
            )

    x = await session.get(Product, product_id)
    x.active = False

    await session.commit()
    await session.refresh(x)

    return x


async def update_product_db(
        product_id: int,
        name: str = None,
        barcode: str = None,
        units_per_package: int = None,
        size_1: float = None,
        size_2: float = None,
        size_3: float = None,
        weight: float = None,
        volume: float = None,
        packaging_x: float = None,
        packaging_y: float = None,
        packaging_z: float = None,
        packaging_obj: str = None,
        facing_preview: str = None,
        session: AsyncSession = None,
        packaging_type_id:int = None,
        category_id = None
):
    """ Обновляет product по id в бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await update_product_db(
                product_id=product_id,
                name=name,
                barcode=barcode,
                units_per_package=units_per_package,
                size_1=size_1,
                size_2=size_2,
                size_3=size_3,
                weight=weight,
                volume=volume,
                session=session,
                packaging_x = packaging_x,
                packaging_y = packaging_y,
                packaging_z = packaging_z,
                packaging_obj = packaging_obj,
                facing_preview=facing_preview,
                category_id=category_id,
                packaging_type_id=packaging_type_id
            )

    x = await session.get(Product, product_id)

    if name:
        x.name = name
    if barcode:
        x.barcode = barcode
    if units_per_package:
        x.units_per_package = units_per_package
    if size_1:
        x.size_1 = size_1
    if size_2:
        x.size_2 = size_2
    if size_3:
        x.size_3 = size_3
    if weight:
        x.weight = weight
    if volume:
        x.volume = volume
    if packaging_x:
        x.packaging_x = packaging_x
    if packaging_y:
        x.packaging_y = packaging_y
    if packaging_z:
        x.packaging_z = packaging_z
    if packaging_obj:
        x.packaging_obj = packaging_obj
    if facing_preview:
        x.facing_preview = facing_preview
    if category_id:
        x.category_id = category_id
    if packaging_type_id:
        x.packaging_type_id = packaging_type_id
    await session.commit()
    await session.refresh(x)

    return x


async def get_products_by_client_db(client_id: int, session: AsyncSession=None):
    """ Возвращает все продукты по id клиента в kwargs """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_products_by_client_db(client_id=client_id, session=session)

    result = await session.execute(select(Product).where(Product.active == True).where(Product.client_id == client_id).order_by(Product.id))

    return result.scalars().all()


async def get_productcategories_db(session: AsyncSession = None):
    """ Возвращает все productcategories из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_productcategories_db(session)

    result = await session.execute(select(ProductCategory).where(ProductCategory.active == True).order_by(ProductCategory.id))

    return result.scalars().all()


async def get_packagingtypes_db(session: AsyncSession = None):
    """ Возвращает все packagingtypes из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_packagingtypes_db(session)

    result = await session.execute(select(PackagingType).where(PackagingType.active == True).order_by(PackagingType.id))

    return result.scalars().all()




async def get_products_db(session: AsyncSession = None):
    """ Возвращает все продукты из бд """
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_products_db(session)

    result = await session.execute(select(Product).where(Product.active == True).order_by(Product.id))

    return result.scalars().all()


async def get_product_db(product_id: int, session: AsyncSession = None):
    """ Возвращает product по id из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_product_db(product_id=product_id, session=session)

    result = await session.get(Product, product_id)

    return result



async def get_product_categories_db(session:AsyncSession=None):
    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await get_product_categories_db(session=session)
    result = await session.execute(select(ProductCategory).order_by(ProductCategory.id))
    return result.scalars().all()