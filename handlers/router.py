from fastapi import APIRouter


project_router = APIRouter(
    tags=["Project operations"]
)

shelf_router = APIRouter(
    tags=["Shelf operations"]
)

product_router = APIRouter(
    tags=["Product operations"]
)

convert_router = APIRouter(
    prefix="/file",
    tags=["Converting operations"]
)

pdf_make_router = APIRouter(
    prefix="/pdf_maker",
    tags=["PdfMaker"]
)