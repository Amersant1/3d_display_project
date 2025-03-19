import os
import uuid
import aiofiles

from fastapi import FastAPI, Request, HTTPException, Response, status, UploadFile
from fastapi.responses import FileResponse

from utils.good_png_maker import change_black_to_transparent
from utils.converter.converter import convert_from_obj_to_svg

from .router import product_router as base_router
from database import *
from . import schemas


MEDIA_DIR = "media"


@base_router.post("/uploadfile")
async def create_upload_file(file: UploadFile,save_name):
    file_name = str(uuid.uuid4())
    
    if save_name:
        file_name = file.filename.split('.')[0]

        
    extension = file.filename.split('.')[1]

    async with aiofiles.open(f"{MEDIA_DIR}/{file_name}.{extension}", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write



    result = {
        "status": "ok",
        "original_file": f"/loadfile/{file_name}.{extension}"
    }

    if extension == "jpg":
        change_black_to_transparent(
            f"{MEDIA_DIR}/{file_name}.{extension}",
            f"{MEDIA_DIR}/{file_name}.png"
        )
        result["png_file"] = f"/loadfile/{file_name}.png"
    elif extension == "obj":
        convert_from_obj_to_svg(
            f"{MEDIA_DIR}/{file_name}.{extension}",
            filename=file_name,
            directory=MEDIA_DIR
        )
        result["front_svg_file"] = f"{file_name}_front.svg"
        result["side_svg_file"] = f"{file_name}_side.svg"
        result["top_svg_file"] = f"{file_name}_top.svg"

    return result


@base_router.get("/loadfile/{file_path}")
async def load_file(file_path: str):
    try:
        file_path = f"{MEDIA_DIR}/{file_path}"
        print(file_path)

        if os.path.isfile(file_path):
            if file_path.split(".")[1]=="svg":
                result = FileResponse(file_path)
                return result
            result = FileResponse(file_path,media_type='application/octet-stream')
            print(result)
            return result
        else:
            print("FAIL")
            return {"status": "fail", "error": f"no such file"}
    except Exception as e:
        print(e)


# ALLOWED_PACKAGING_TYPES = [
#     "1: Овал/Blister",
#     "2: Короб",
#     "3: Спичечный",
#     "4: Подвесной",
#     "5: Накопочный короб"
# ]


@base_router.post("/packagingtype", status_code=status.HTTP_201_CREATED)
async def create_packagingtype(data: schemas.CreatePackagingType, response: Response):
    # if data.name not in ALLOWED_PACKAGING_TYPES:
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    #     return {"status": "fail", "error": f"packagingtype_name should be one of {ALLOWED_PACKAGING_TYPES}"}

    result = await create_packagingtype_db(
        data=dict(data.dict())
    )

    return {"status": "ok", "packagingtype_id": result}


@base_router.put("/packagingtype_{packagingtype_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_packagingtype(packagingtype_id: int, data: schemas.UpdatePackagingType, response: Response):
    try:
        result = await update_packagingtype_db(
            name=data.name,
            front_svg=data.front_svg,
            side_svg=data.side_svg,
            top_svg=data.top_svg,
            packagingtype_id=packagingtype_id,
            object=data.object
        )
        return {"status": "ok", "packagingtype": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such packagingtype_id"}


@base_router.delete("/packagingtype_{packagingtype_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_packagingtype(packagingtype_id: int, response: Response):
    try:
        result = await delete_packagingtype_db(
            packagingtype_id=packagingtype_id
        )
        return {"status": "ok", "packagingtype": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such packagingtype_id"}


@base_router.get("/packagingtypes")
async def get_packagingtypes():
    result = await get_packagingtypes_db()
    return {"status": "ok", "packagingtypes": result}


@base_router.post("/productcategory", status_code=status.HTTP_201_CREATED)
async def create_productcategory(data: schemas.ProductCategory, response: Response):
    result = await create_productcategory_db(
        name=data.name
    )

    return {"status": "ok", "productcategory_id": result}


@base_router.put("/productcategory_{productcategory_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_productcategory(productcategory_id: int, data: schemas.ProductCategory, response: Response):
    try:
        result = await update_productcategory_db(
            name=data.name, productcategory_id=productcategory_id
        )
        return {"status": "ok", "productcategory": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such productcategory_id"}


@base_router.get("/product_categories")
async def get_product_categories():
    result = await get_product_categories_db()
    return {"status": "ok", "product_categories": result}

@base_router.delete("/productcategory_{productcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_productcategory(productcategory_id: int, response: Response):
    try:
        result = await delete_productcategory_db(
            productcategory_id=productcategory_id
        )
        return {"status": "ok", "productcategory": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such productcategory_id"}


@base_router.get("/productcategories")
async def get_productcategories():
    result = await get_productcategories_db()
    return {"status": "ok", "productcategories": result}


@base_router.post("/product", status_code=status.HTTP_201_CREATED)
async def create_product(data: schemas.CreateProduct, response: Response):
    result = await create_product_db(
        data=dict(data.dict())
    )

    return {"status": "ok", "product_id": result}


@base_router.delete("/product_{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, response: Response):
    try:
        result = await delete_product_db(
            product_id=product_id
        )
        return {"status": "ok", "product": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such product_id"}


@base_router.put("/product_{product_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_product(product_id: int, data: schemas.UpdateProduct, response: Response):
    try:
        result = await update_product_db(
            product_id=product_id,
            name=data.name,
            barcode=data.barcode,
            units_per_package=data.units_per_package,
            size_1=data.size_1,
            size_2=data.size_2,
            size_3=data.size_3,
            weight=data.weight,
            volume=data.volume,
            category_id = data.category_id,
            facing_preview=data.facing_preview,
            packaging_type_id=data.packaging_type_id
        )
        return {"status": "ok", "product": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such product_id"}


@base_router.get("/products")
async def get_products():
    result = await get_products_db()
    return {"status": "ok", "products": result}


@base_router.get("/productsbyclient")
async def get_products_by_client(client_id: int):
    result = await get_products_by_client_db(client_id=client_id)
    if result:
        return {"status": "ok", "products": result}
    return {"status": "ok", "products": []}



@base_router.get("/product_{product_id}")
async def get_product(product_id: int, response: Response):
    result = await get_product_db(product_id=product_id)
    if result:
        return {"status": "ok", "product": result}
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"status": "fail", "error": "no such product_id"}


@base_router.post("/productonshelf", status_code=status.HTTP_201_CREATED)
async def create_productonshelf(data: schemas.CreateProductOnShelf):
    result = await create_productonshelf_db(
        shelf_id=data.shelf_id,
        product_id=data.product_id
    )

    return {"status": "ok", "productonshelf_id": result}


@base_router.delete("/productonshelf_{productonshelf_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_productonshelf(productonshelf_id: int):
    result = await delete_productonshelf_db(
        productonshelf_id=productonshelf_id
    )

    return {"status": "ok", "productonshelf": result}
