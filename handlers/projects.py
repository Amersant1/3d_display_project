from fastapi import FastAPI, Request, HTTPException, Response, status

from .router import project_router as base_router
from database import *
from . import schemas


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
async def clone_model(model: str, instance_id: int, response: Response):
    if model not in ALLOWED_MODEL_NAMES:
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
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"status": "fail", "error": "no such model"}

        return {"status": "ok", "new_instance_type": model, "new_instances": new_instances}
    except Exception as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": error}


@base_router.put("/employee_{employee_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_employee(employee_id: int, data: schemas.CreateEmployee, response: Response):
    try:
        result = await update_employee_db(
            full_name=data.full_name, employee_id=employee_id
        )
        return {"status": "ok", "employee": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such employee_id"}


@base_router.put("/client_{client_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_client(client_id: int, data: schemas.UpdateClient, response: Response):
    try:
        result = await update_client_db(
            name=data.name, client_id=client_id
        )
        return {"status": "ok", "client": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such client_id"}


@base_router.delete("/employee_{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, response: Response):
    try:
        result = await delete_employee_db(
            employee_id=employee_id
        )
        return {"status": "ok", "employee": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such employee_id"}


@base_router.delete("/client_{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, response: Response):
    try:
        result = await delete_client_db(
            client_id=client_id
        )
        return {"status": "ok", "client": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such client_id"}


@base_router.post('/create_client', status_code=status.HTTP_201_CREATED)
async def create_client(request: Request, data: schemas.UpdateClient):
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
async def create_employee(request: Request, data: schemas.CreateEmployee):
    employee_id = await add_employee_db(data.full_name)
    return {"status": "ok", "employee_id": employee_id}


@base_router.post("/create_project", status_code=status.HTTP_201_CREATED)
async def create_project(data: schemas.AddProject):
    if not (data.client_id or data.client_name):
        return {"status": "fail", "error": "You must provide either client_id or name"}
    project_id = await create_project_db(
        data.name,
        client_id=data.client_id,
        client_name=data.client_name
    )
    return {"status": "ok", "project_id": project_id}


@base_router.put("/project_{project_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_project(project_id: int, data: schemas.UpdateProject, response: Response):
    try:
        result = await update_project_db(
            project_id=project_id, name=data.name, client_id=data.client_id
        )
        return {"status": "ok", "project": result}
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "fail", "error": "no such project_id"}


@base_router.delete("/project_{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, response: Response):
    try:
        result = await delete_project_db(
            project_id=project_id
        )
        return {"status": "ok", "project": result}
    except:
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
