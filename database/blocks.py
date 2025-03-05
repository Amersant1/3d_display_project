from sqlalchemy import select

from model import *


async def create_productonshelf_db(shelf_id: int, product_id: int, session: AsyncSession=None):
    """ Создает добавление продукта на полку """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await create_productonshelf_db(
                shelf_id=shelf_id,
                product_id=product_id,
                session=session
            )

    res = ProductOnShelf(
        shelf_id=shelf_id,
        product_id=product_id
    )
    session.add(res)
    await session.commit()
    await session.refresh(res)
    return res.id


async def delete_productonshelf_db(productonshelf_id: int, session: AsyncSession = None):
    """ Возвращает product по id из бд """

    if session is None:
        # Create a new session if one is not provided
        async for session in make_session():
            return await delete_productonshelf_db(productonshelf_id=productonshelf_id, session=session)

    res = await session.get(ProductOnShelf, productonshelf_id)
    await session.delete(res)
    await session.commit()
    return []
