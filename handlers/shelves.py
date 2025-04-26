from fastapi import FastAPI, Request, HTTPException, Response, status

from .router import shelf_router as base_router
from database import *
from . import schemas


SHELVES_REQUESTS = []


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
async def delete_preptype(preptype_id: int, response: Response = None):
    try:
        result = await delete_preptype_db(
            preptype_id=preptype_id
        )
        return {"status": "ok", "preptype": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such preptype_id"}


@base_router.put("/preptype_{preptype_id}", status_code=status.HTTP_201_CREATED)
async def update_preptype(preptype_id: int, data: schemas.UpdatePrepType):

    result = await update_preptype_db(
        name=data.name,
        preptype_id=preptype_id,
        created=data.created
    )

    return {"status": "ok", "preptype": result}


@base_router.post("/preptype", status_code=status.HTTP_201_CREATED)
async def create_preptype(data: schemas.CreatePrepType):
    # if data.name not in ALLOWED_PREP_TYPES:
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
async def create_poultice(data: schemas.CreatePoultice, session_name: str = "", original_id: int = 0):

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
        json_sizes_box=data.json_sizes_box,

        number_of_shelves=data.number_of_shelves,
        width_mm=data.width_mm,
        depth_mm=data.depth_mm,
        sides_height_mm=data.sides_height_mm,
        sides_width_mm=data.sides_width_mm,
        back_width_mm=data.back_width_mm,
        front_width_mm=data.front_width_mm,
        shelf_width_mm=data.shelf_width_mm,
        fronton_height_mm=data.fronton_height_mm,
        topper_height_mm=data.topper_height_mm,

        session_name=session_name,
        original_id=original_id
    )

    return {"status": "ok", "poultice_id": result}


@base_router.delete("/poultice_{poultice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_poultice(poultice_id: int, session_name: str = "", response: Response = None):
    try:
        if session_name != "":
            elems = await get_poultice_by_session_id(poultice_id, session_name)

            try:
                orig_poul = elems[0]
            except IndexError:
                if response: response.status_code = status.HTTP_400_BAD_REQUEST
                return {"status": "fail", "error": "wrong session name"}

            result = await delete_poultice_db(
                poultice_id=orig_poul.id
            )
            return {"status": "ok", "poultice": result}
        result = await delete_poultice_db(
            poultice_id=poultice_id
        )
        return {"status": "ok", "poultice": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such poultice_id"}


@base_router.put("/poultice_{poultice_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_poultice(poultice_id: int, data: schemas.UpdatePoultice, response: Response=None, session_name: str = "", execNow: bool = False):
    global SHELVES_REQUESTS

    if execNow:
        # try:
            if session_name != "":
                elems = await get_poultice_by_session_id(poultice_id, session_name)
                if len(elems) == 0:
                    orig_poul = (await get_poultice_db(poultice_id))[0]
                    data = {
                        "project_id": data.project_id if data.project_id else orig_poul.project_id,
                        "file": data.file if data.file else orig_poul.file,
                        "size_x": data.size_x if data.size_x else orig_poul.size_x,
                        "size_y": data.size_y if data.size_y else orig_poul.size_y,
                        "size_z": data.size_z if data.size_z else orig_poul.size_z,
                        "is_designed": data.is_designed if data.is_designed else orig_poul.is_designed,
                        "name": data.name if data.name else orig_poul.name,
                        "image": data.image if data.image else orig_poul.image,
                        "number": data.number if data.number else orig_poul.number,
                        "type_id": data.type_id if data.type_id else orig_poul.type_id,
                        "json_sizes_box": data.json_sizes_box if data.json_sizes_box else orig_poul.json_sizes_box,
                        "number_of_shelves": data.number_of_shelves if data.number_of_shelves else orig_poul.number_of_shelves,
                        "width_mm": data.width_mm if data.width_mm else orig_poul.width_mm,
                        "depth_mm": data.depth_mm if data.depth_mm else orig_poul.depth_mm,
                        "sides_height_mm": data.sides_height_mm if data.sides_height_mm else orig_poul.sides_height_mm,
                        "sides_width_mm": data.sides_width_mm if data.sides_width_mm else orig_poul.sides_width_mm,
                        "back_width_mm": data.back_width_mm if data.back_width_mm else orig_poul.back_width_mm,
                        "front_width_mm": data.front_width_mm if data.front_width_mm else orig_poul.front_width_mm,
                        "shelf_width_mm": data.shelf_width_mm if data.shelf_width_mm else orig_poul.shelf_width_mm,
                        "fronton_height_mm": data.fronton_height_mm if data.fronton_height_mm else orig_poul.fronton_height_mm,
                        "topper_height_mm": data.topper_height_mm if data.topper_height_mm else orig_poul.topper_height_mm,
                        "session_name": session_name,
                        "original_id": orig_poul.id
                    }
                    result = await create_poultice_db(
                        **data
                    )
                    result = (await get_poultice_db(result))[0]
                    return {"status": "ok", "poultice": result}
                else:
                    poultice = elems[0]
                    poultice_id = poultice.id
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
                json_sizes_box = data.json_sizes_box,

                number_of_shelves = data.number_of_shelves,
                width_mm = data.width_mm,
                depth_mm = data.depth_mm,
                sides_height_mm = data.sides_height_mm,
                sides_width_mm = data.sides_width_mm,
                back_width_mm = data.back_width_mm,
                front_width_mm = data.front_width_mm,
                shelf_width_mm = data.shelf_width_mm,
                fronton_height_mm = data.fronton_height_mm,
                topper_height_mm = data.topper_height_mm,

                created = data.created
            )
            return {"status": "ok", "poultice": result}
        # except:
            if response:
                response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "fail", "error": "no such poultice_id"}
    else:
        SHELVES_REQUESTS.append({
            "operation": "update_poultice",
            "data": data,
            "poultice_id": poultice_id
        })

        return {"status": "ok"}


@base_router.get("/poultice_{poultice_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_poultice(poultice_id: int, response: Response, session_name: str = ""):
    try:
        result = await get_poultice_db(
            poultice_id=poultice_id,
            session_name=session_name
        )
        return {"status": "ok", "poultice": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such poultice_id"}


@base_router.get("/poultices")
async def get_poultices():
    result = await get_poultices_db()
    return {"status": "ok", "poultices": result}

@base_router.post("/copy_poultice")
async def copy_poultice(data:schemas.Copy):
    data = dict(data.dict())
    copy_id = data["id"]
    result = await copy_poultice_in_db(copy_id=copy_id)
    return result

@base_router.get("/poultice_{poultice_id}")
async def get_poultice(poultice_id: int, session_name: str = ""):
    result = await get_poultice_db(poultice_id=poultice_id, session_name=session_name)
    if result:
        return {"status": "ok", "poultice": result}
    return {"status": "fail", "error": "no such project_id"}


@base_router.get("/poultice")
async def get_poultice_by_project(project_id: int, session_name: str = ""):
    result = await get_poultice_by_project_db(project_id=project_id, session_name=session_name)
    if result:
        return {"status": "ok", "poultices": result}
    return {"status": "ok", "poultices": []}


@base_router.post("/shelf", status_code=status.HTTP_201_CREATED)
async def create_shelf(data: schemas.CreateShelf, session_name: str = "", original_id=0, execNow: bool = False):
    global SHELVES_REQUESTS

    if execNow:
        data = dict(data.dict())
        data["session_name"] = session_name
        data["original_id"] = original_id
        result = await create_shelf_db(
            data=data
        )

        return {"status": "ok", "shelf_id": result}
    else:
        SHELVES_REQUESTS.append({
            "operation": "create",
            "data": data
        })
        return {"status": "ok"}


@base_router.get("/shelves")
async def get_shelves_by_poultice(poultice_id: int, session_name: str = ""):
    result = await get_shelf_by_poultice_db(poultice_id=poultice_id, session_name=session_name)
    if result:
        return {"status": "ok", "shelves": result}
    return {"status": "ok", "shelves": []}


@base_router.get("/get_all_shelves")
async def get_all_shelves():
    result = await get_all_shelves_db()
    return {"status": "ok", "shelves": result}


@base_router.delete("/shelf_{shelf_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf(shelf_id: int, response: Response = None, session_name: str = "", execNow: bool = False):
    global SHELVES_REQUESTS

    if execNow:
        try:
            # if session_name != "":

            elems = await get_shelf_by_session_id(shelf_id, session_name)
            if len(elems) > 0:

                try:
                    orig_shelf = elems[0]
                except IndexError:
                    if response: response.status_code = status.HTTP_400_BAD_REQUEST
                    return {"status": "fail", "error": "wrong session name"}

                result = await delete_shelf_db(
                    shelf_id=orig_shelf.id
                )

            else:
                result = await delete_shelf_db(
                    shelf_id=shelf_id
                )
            return {"status": "ok", "shelf": result}
            # result = await delete_shelf_db(
            #     shelf_id=shelf_id
            # )
            # return {"status": "ok", "shelf": result}
        except:
            if response:
                response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "fail", "error": "no such shelf_id"}
    else:
        SHELVES_REQUESTS.append({
            "operation": "delete",
            "shelf_id": shelf_id
        })
        return {"status": "ok"}


@base_router.put("/shelf_{shelf_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_shelf(shelf_id: int, data: schemas.UpdateShelf, response: Response = None, session_name: str = "", execNow: bool = False):
    global SHELVES_REQUESTS

    if execNow:
        try:
            if hasattr(data, 'json_rows'):
                if isinstance(data.json_rows,list):
                    data.json_rows={}
                    # data.json_rows = dict()
            if session_name != "":
                elems = await get_shelf_by_session_id(shelf_id, session_name)
                if len(elems) == 0:
                    orig_shelf = (await get_shelf_by_shelf_id(shelf_id))[0]
                    data = {
                        "width": data.width if data.width else orig_shelf.width,
                        "length": data.length if data.length else orig_shelf.length,
                        "heigth": data.heigth if data.heigth else orig_shelf.heigth,
                        "margin_top": data.margin_top if data.margin_top else orig_shelf.margin_top,
                        "margin_bottom": data.margin_bottom if data.margin_bottom else orig_shelf.margin_bottom,
                        "poulticle_id": orig_shelf.poulticle_id,
                        "isRows": data.isRows if data.isRows else orig_shelf.isRows,
                        "json_shelf": data.json_shelf if data.json_shelf else orig_shelf.json_shelf,
                        "json_rows": data.json_rows if data.json_rows else orig_shelf.json_rows,
                        "session_name": session_name,
                        "original_id": orig_shelf.id
                    }
                    result = await create_shelf_db(
                        data=data
                    )
                    result = (await get_shelf_by_shelf_id(result))[0]
                    return {"status": "ok", "shelf": result}
                else:
                    shelf = elems[0]
                    shelf_id = shelf.id

            result = await update_shelf_db(
                shelf_id=shelf_id,
                width=data.width,
                length=data.length,
                heigth=data.heigth,
                margin_top=data.margin_top,
                margin_bottom=data.margin_bottom,
                json_shelf=data.json_shelf,
                json_rows=data.json_rows,
                active = data.active,
                isRows = data.isRows,
                created = data.created
            )
            return {"status": "ok", "shelf": result}
        except:
            if response:
                response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "fail", "error": "no such shelf_id"}
    else:
        SHELVES_REQUESTS.append({
            "operation": "update",
            "shelf_id": shelf_id,
            "data": data
        })
        return {"status": "ok"}


@base_router.get("/shelf_{shelf_id}", status_code=status.HTTP_202_ACCEPTED)
async def get_shelf_by_id(shelf_id: int, response: Response, session_name: str = ""):
    try:
        result = await get_shelf_by_shelf_id(
            shelf_id=shelf_id,
            session_name=session_name
        )
        return {"status": "ok", "shelf": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such shelf_id"}


@base_router.get('/all_shelves')
async def get_shelves():
    result = await get_shelves_db()
    return {"status": "ok", "shelves": result}


@base_router.get('/check_sessions')
async def check_sessions(poultice_id: int):
    """ WARNING: CAN BE NOT CORRECT YET! """
    poultices, shelves = await check_sessions_db(poultice_id=poultice_id)

    result = set()
    for el in poultices:
        result.add(el.session_name)
    for el in shelves:
        result.add(el.session_name)

    return {"status": "ok", "valid_sessions": result}


@base_router.post("/commit_session")
async def commit_session(session_name: str):
    try:
        await commit_session_db(session_name)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "fail", "error": e}


@base_router.post("/save_shelves")
async def save_shelves():
    global SHELVES_REQUESTS

    try:
        for el in SHELVES_REQUESTS:
            operation = el["operation"]
            # print(el)

            if operation == "create":
                await create_shelf(data=el["data"], execNow=True)
            elif operation == "update":
                await update_shelf(data=el["data"], shelf_id=el["shelf_id"], execNow=True)
            elif operation == "delete":
                await delete_shelf(shelf_id=el["shelf_id"], execNow=True)
            elif operation == "update_poultice":
                await update_poultice(poultice_id=el["poultice_id"], data=el["data"], execNow=True)

        SHELVES_REQUESTS = []
        return {"status": "ok"}
    except Exception as e:
        SHELVES_REQUESTS = []
        return {"status": "fail", "error": e}
