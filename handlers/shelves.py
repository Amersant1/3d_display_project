from fastapi import FastAPI, Request, HTTPException, Response, status

from .router import shelf_router as base_router
from database import *
from . import schemas


ALLOWED_PREP_TYPES = [
    "1/4 напольный патент",
    "1/4 напольный эконом",
    "1/4 напольный на держателях",
    "1/4 напольный обейджик",
    "1/8 напольный патент",
    "1/8 напольный эконом",
    "1/8 напольный на держателях",
    "1/8 напольный обейджик",
    "Подвесной"
]


@base_router.delete("/preptype_{preptype_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_preptype(preptype_id: int, response: Response):
    try:
        result = await delete_preptype_db(
            preptype_id=preptype_id
        )
        return {"status": "ok", "preptype": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such preptype_id"}


@base_router.put("/preptype_{preptype_id}", status_code=status.HTTP_201_CREATED)
async def update_preptype(preptype_id: int, data: schemas.CreatePrepType, response: Response):

    result = await update_preptype_db(
        name=data.name,
        preptype_id=preptype_id
    )

    return {"status": "ok", "preptype": result}


@base_router.post("/preptype", status_code=status.HTTP_201_CREATED)
async def create_preptype(data: schemas.CreatePrepType, response: Response):
    # if data.name not in ALLOWED_PREP_TYPES:
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    #     return {"status": "fail", "error": f"preptype_name should be one of {ALLOWED_PREP_TYPES}"}

    result = await create_preptype_db(
        data=dict(data.dict())
    )

    return {"status": "ok", "preptype_id": result}


@base_router.get("/preptypes")
async def get_preptypes():
    result = await get_preptypes_db()
    return {"status": "ok", "preptypes": result}



@base_router.post("/poultice", status_code=status.HTTP_201_CREATED)
async def create_poultice(data: schemas.CreatePoultice, response: Response):

    result = await create_poultice_db(
        project_id=data.project_id,
        file=data.file,
        type_id=data.type_id,
        size_x=data.size_x,
        size_y=data.size_y,
        size_z=data.size_z,
        name=data.name,
        image=data.image,
        number=data.number,
        json_sizes_box=data.json_sizes_box
    )

    return {"status": "ok", "poultice_id": result}


@base_router.delete("/poultice_{poultice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_poultice(poultice_id: int, response: Response):
    try:
        result = await delete_poultice_db(
            poultice_id=poultice_id
        )
        return {"status": "ok", "poultice": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such poultice_id"}


@base_router.put("/poultice_{poultice_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_poultice(poultice_id: int, data: schemas.UpdatePoultice, response: Response):

    try:
        result = await update_poultice_db(
            poultice_id=poultice_id,
            project_id=data.project_id,
            file=data.file,
            size_x=data.size_x,
            size_y=data.size_y,
            size_z=data.size_z,
            type=None,
            is_designed=data.is_designed,
            name=data.name,
            image=data.image,
            number=data.number,
            type_id=data.type_id,
            json_sizes_box = data.json_sizes_box
        )
        return {"status": "ok", "poultice": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such poultice_id"}


@base_router.get("/poultice_{poultice_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_poultice(poultice_id: int, response: Response):

    try:
        result = await get_poultice_db(
            poultice_id=poultice_id,
            
        )
        return {"status": "ok", "poultice": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such poultice_id"}




@base_router.get("/poultices")
async def get_poultices():
    result = await get_poultices_db()
    return {"status": "ok", "poultices": result}


@base_router.get("/poultice_{poultice_id}")
async def get_poultice(poultice_id: int):
    result = await get_poultice_db(poultice_id=poultice_id)
    if result:
        return {"status": "ok", "poultice": result}
    return {"status": "fail", "error": "no such project_id"}


@base_router.get("/poultice")
async def get_poultice_by_project(project_id: int):
    result = await get_poultice_by_project_db(project_id=project_id)
    if result:
        return {"status": "ok", "poultices": result}
    return {"status": "fail", "poultices": []}


@base_router.post("/shelf", status_code=status.HTTP_201_CREATED)
async def create_shelf(data: schemas.CreateShelf):
    result = await create_shelf_db(
        data=dict(data.dict())
    )

    return {"status": "ok", "shelf_id": result}


@base_router.get("/shelves")
async def get_shelves_by_poultice(poultice_id: int):
    result = await get_shelf_by_poultice_db(poultice_id=poultice_id)
    if result:
        return {"status": "ok", "shelves": result}
    return {"status": "fail", "shelves": []}


@base_router.get("/get_all_shelves")
async def get_all_shelves():
    result = await get_all_shelves_db()
    return {"status": "ok", "shelves": result}


@base_router.delete("/shelf_{shelf_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf(shelf_id: int, response: Response):
    try:
        result = await delete_shelf_db(
            shelf_id=shelf_id
        )
        return {"status": "ok", "shelf": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such shelf_id"}


@base_router.put("/shelf_{shelf_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_shelf(shelf_id: int, data: schemas.UpdateShelf, response: Response):
    try:
        
        result = await update_shelf_db(
            shelf_id=shelf_id,
            width=data.width,
            length=data.length,
            heigth=data.heigth,
            margin_top=data.margin_top,
            margin_bottom=data.margin_bottom,
            json_shelf=data.json_shelf,
            json_rows=data.json_rows
        )
        return {"status": "ok", "shelf": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such shelf_id"}


@base_router.get("/shelf_{shelf_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_shelf_by_id(shelf_id: int, response: Response):
    try:
        result = await get_shelf_by_shelf_id(
            shelf_id=shelf_id,
        )
        return {"status": "ok", "shelf": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such shelf_id"}


@base_router.get('/all_shelves')
async def get_shelves():
    result = await get_shelves_db()
    return {"status": "ok", "shelves": result}