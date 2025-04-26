from fastapi import FastAPI, Request, HTTPException, Response, status
from typing import List
import json

from .router import project_router as base_router
from database import *
from . import schemas

from handlers import shelves as sh
from handlers import products as pr


ALLOWED_MODEL_NAMES = [
    "client",
    "employee",
    "packaging_type",
    "prep_type",
    "product_category",
    "project",
    "poultice",
    "shelf",
    "product"
]


@base_router.post("/clone_{model}_{instance_id}", status_code=status.HTTP_201_CREATED)
async def clone_model(model: str, instance_id: int, response: Response = None):
    if model not in ALLOWED_MODEL_NAMES:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": f"model should be one of: {ALLOWED_MODEL_NAMES}"}


    try:
        new_instances: list

        if model == "client":
            new_instances = await clone_client_db(instance_id)
        elif model == "employee":
            new_instances = await clone_employee_db(instance_id)
        elif model == "packaging_type":
            new_instances = await clone_packaging_type_db(instance_id)
        elif model == "prep_type":
            new_instances = await clone_prep_type_db(instance_id)
        elif model == "product_category":
            new_instances = await clone_product_category_db(instance_id)
        elif model == "project":
            new_instances = await clone_project_db(instance_id)
        elif model == "poultice":
            new_instances = await clone_poultice_db(instance_id)
        elif model == "shelf":
            new_instances = await clone_shelf_db(instance_id)
        elif model == "product":
            new_instances = await clone_product_db(instance_id)
        else:
            if response:
                response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "fail", "error": "no such model"}

        return {"status": "ok", "new_instance_type": model, "new_instances": new_instances}
    except Exception as error:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": error}


@base_router.put("/employee_{employee_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_employee(employee_id: int, data: schemas.UpdateEmployee, response: Response = None):
    try:
        result = await update_employee_db(
            full_name=data.full_name, employee_id=employee_id, created=data.created
        )
        return {"status": "ok", "employee": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such employee_id"}


@base_router.put("/client_{client_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_client(client_id: int, data: schemas.UpdateClient, response: Response = None):
    try:
        result = await update_client_db(
            created=data.created,
            name=data.name,
            client_id=client_id
        )
        return {"status": "ok", "client": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such client_id"}


@base_router.delete("/employee_{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, response: Response = None):
    try:
        result = await delete_employee_db(
            employee_id=employee_id
        )
        return {"status": "ok", "employee": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such employee_id"}


@base_router.delete("/client_{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, response: Response = None):
    try:
        result = await delete_client_db(
            client_id=client_id
        )
        return {"status": "ok", "client": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such client_id"}


@base_router.post('/create_client', status_code=status.HTTP_201_CREATED)
async def create_client(data: schemas.CreateClient):
    client_id = await add_client_db(data.name)
    return {"status": "ok", "client_id": client_id}


@base_router.get("/clients")
async def get_clients():
    result = await get_clients_db()
    return {"status": "ok", "clients": result}


@base_router.get("/employees")
async def get_employees():
    result = await get_employees_db()
    return {"status": "ok", "employees": result}


@base_router.post('/create_employee', status_code=status.HTTP_201_CREATED)
async def create_employee(data: schemas.CreateEmployee):
    employee_id = await add_employee_db(data.full_name)
    return {"status": "ok", "employee_id": employee_id}


@base_router.post("/create_project", status_code=status.HTTP_201_CREATED)
async def create_project(data: schemas.AddProject):
    if not (data.client_id or data.client_name):
        return {"status": "fail", "error": "You must provide either client_id or name"}
    project_id = await create_project_db(
        data.name,
        client_id=data.client_id,
        client_name=data.client_name,
        number=data.number
    )
    return {"status": "ok", "project_id": project_id}


@base_router.put("/project_{project_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_project(project_id: int, data: schemas.UpdateProject, response: Response = None):
    try:
        result = await update_project_db(
            project_id=project_id, name=data.name, client_id=data.client_id, created=data.created,number=data.number
        )
        return {"status": "ok", "project": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such project_id"}


@base_router.delete("/project_{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, response: Response = None):
    try:
        result = await delete_project_db(
            project_id=project_id
        )
        return {"status": "ok", "project": result}
    except:
        if response:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such project_id"}


@base_router.get("/project_{project_id}")
async def get_project(project_id: int):
    result = await get_project_db(project_id=project_id)
    if result:
        return {"status": "ok", "project": result}
    return {"status": "fail", "error": "no such project_id"}


@base_router.get("/projects")
async def get_projects():
    result = await get_projects_db()
    return {"status": "ok", "projects": result}


f"""
[
    "change user id fields field2=value2 && field2=3",
    "delete user id",
    "create user $id fields field1=value1",
    "change user $id fields field=value",
    
    "copy project 1 created project_1=$prid_1 && poultice_100=$pe_1"
]

where $id is newly created ids which client yet don't know
where in copy after created args are in form [ALLOWED MODEL type which is created]_[old instance id]=$var1
"""


@base_router.post("/run_sequence", status_code=status.HTTP_201_CREATED)
async def run_sequence(data: List[str]):
    """
    request example:

    [
        "create project $id fields name=test && client_id=45",
        "change project 177 fields client_id=70 && active=1",
        "delete project 177",
        "change project $id fields name=hello",

        "copy project 1 created project_1=$prid_1 && poultice_100=$pe_1"
    ]
    """

    acc_models = [
        "client",
        "employee",
        "packaging_type",
        "poultice",
        "prep_type",
        "product_category",
        "product",
        "project",
        "shelf",
    ]

    endpoints = {
        "create_client": [create_client, schemas.CreateClient, "client_id"],
        "create_employee": [create_employee, schemas.CreateEmployee, "employee_id"],
        "create_packaging_type": [pr.create_packagingtype, schemas.CreatePackagingType, "packagingtype_id"],
        "create_poultice": [sh.create_poultice, schemas.CreatePoultice, "poultice_id"],
        "create_prep_type": [sh.create_preptype, schemas.CreatePrepType, "preptype_id"],
        "create_product_category": [pr.create_productcategory, schemas.ProductCategory, "productcategory_id"],
        "create_product": [pr.create_product, schemas.CreateProduct, "product_id"],
        "create_project": [create_project, schemas.AddProject, "project_id"],
        "create_shelf": [sh.create_shelf, schemas.CreateShelf, "shelf_id"],

        "change_client": [update_client, schemas.UpdateClient],
        "change_employee": [update_employee, schemas.UpdateEmployee],
        "change_packaging_type": [pr.update_packagingtype, schemas.UpdatePackagingType],
        "change_poultice": [sh.update_poultice, schemas.UpdatePoultice],
        "change_prep_type": [sh.update_preptype, schemas.UpdatePrepType],
        "change_product_category": [pr.update_productcategory, schemas.UpdateProductCategory],
        "change_product": [pr.update_product, schemas.UpdateProduct],
        "change_project": [update_project, schemas.UpdateProject],
        "change_shelf": [sh.update_shelf, schemas.UpdateShelf],

        "delete_client": [delete_client, "client_id"],
        "delete_employee": [delete_employee, "employee_id"],
        "delete_packaging_type": [pr.delete_packagingtype, "packagingtype_id"],
        "delete_poultice": [sh.delete_poultice, "poultice_id"],
        "delete_prep_type": [sh.delete_preptype, "preptype_id"],
        "delete_product_category": [pr.delete_productcategory, "productcategory_id"],
        "delete_product": [pr.delete_product, "product_id"],
        "delete_project": [delete_project, "project_id"],
        "delete_shelf": [sh.delete_shelf, "shelf_id"],

        "copy": [clone_model]
    }

    delayed_endpoints = [
        "create_shelf", "change_shelf", "delete_shelf",
        "change_poultice"
    ]


    response = []
    new_models = {}

    for line in data:
        # try:
            parsed_line = line

            for key in new_models:
                parsed_line = parsed_line.replace(key, new_models[key])

            l = parsed_line.split()

            action = l[0]
            model = l[1]
            model_id = l[2]

            if not model in acc_models:
                response.append(f"error: {model} not accepted. Accepted: {acc_models}")
                break

            endpoint = f"{action}_{model}"


            try:
                args = parsed_line.split(" fields ")[1]
                args = dict(el.split('=') for el in args.split(' && '))
            except:
                args = {}

            dicted_args = [
                'json_rows',
                'json_shelf',
                'json_sizes_box',
            ]

            for el in args:
                if el in dicted_args:
                    args[el] = json.loads(args[el])

            if endpoint in delayed_endpoints:
                args["execNow"] = True

            if action == "create":
                if endpoint in delayed_endpoints:
                    result = (await endpoints[endpoint][0](endpoints[endpoint][1](**args), execNow=True))[endpoints[endpoint][2]]
                else:
                    result = (await endpoints[endpoint][0](endpoints[endpoint][1](**args)))[endpoints[endpoint][2]]
                if model_id.startswith('$'):
                    new_models[model_id] = str(result)
            elif action == "delete":
                args[endpoints[endpoint][1]] = model_id
                await endpoints[endpoint][0](**args)
            elif action == "change":
                if endpoint in delayed_endpoints:
                    print(args)
                    await endpoints[endpoint][0](model_id, data=endpoints[endpoint][1](**args), execNow=True)
                else:
                    await endpoints[endpoint][0](model_id, data=endpoints[endpoint][1](**args))
            elif action == "copy":
                result = await endpoints[action][0](model=model, instance_id=model_id)
                try:
                    created_asked = parsed_line.split(" created ")[1]
                    created_asked = created_asked.split(' && ')
                    created_asked = [el.split('=') for el in created_asked]
                except:
                    created_asked = []
                # print(created_asked)

                for created_asked_tuple in created_asked:
                    if not created_asked_tuple[1].startswith('$'):
                        continue

                    old_model = "_".join(created_asked_tuple[0].split('_')[0:-1])
                    old_model_id = created_asked_tuple[0].split('_')[-1]
                    # print(old_model, old_model_id)
                    # old_model, old_model_id = created_asked_tuple[0].split('_')

                    for new_instance in result["new_instances"]:
                        if (new_instance["type"] == old_model) and (new_instance["old_id"] == int(old_model_id)):
                            new_models[created_asked_tuple[1]] = str(new_instance["id"])
                            break

                    print(new_models)

            response.append(f"ok: {parsed_line}")
        # except Exception as e:
        #     response.append(f"fail {e}: {parsed_line}")
            # break

    return {"status": "ok", "status": response}
