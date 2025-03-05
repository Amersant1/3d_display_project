from enum import Enum

from pydantic import BaseModel, Json
from pydantic import field_validator
from pydantic.dataclasses import dataclass
from typing import Optional, List, Any,Dict


class CreateEmployee(BaseModel):
    full_name: str


class UpdateClient(BaseModel):
    name: str


class AddProject(BaseModel):
    name: str
    client_id: Optional[int] = None
    client_name: Optional[str] = None

    # TODO: Validation if client id or name is given not by if in view controller
    """
    @field_validator('client_name')
    @classmethod
    def check_id_or_name(self, v, values):
        if 'client_id' not in values and not self.client_name:
            raise ValueError('either a or b is required')
        return self.client_name
    """


class UpdateProject(BaseModel):
    name: Optional[str] = None
    client_id: Optional[int] = None


class Prep_Type(Enum):
    type1 = "1/4 напольный патент"
    type2 = "1/4 напольный эконом"
    type3 = "1/4 напольный на держателях"
    type4 = "1/4 напольный обейджик"
    type5 = "1/8 напольный патент"
    type6 = "1/8 напольный эконом"
    type7 = "1/8 напольный на держателях"
    type8 = "1/8 напольный обейджик"
    type9 = "Подвесной"


class CreatePoultice(BaseModel):
    project_id: int
    file: Optional[str] = None
    type_id: int

    size_x: float
    size_y: float
    size_z: float

    name: str
    image: str
    number: int

    json_sizes_box: Optional[Dict[str, Any]] = None


class UpdatePoultice(BaseModel):
    project_id: Optional[int] = None
    file: Optional[str] = None
    type_id: Optional[int] = None
    size_x: Optional[float] = None
    size_y: Optional[float] = None
    size_z: Optional[float] = None

    name: Optional[str] = None
    image: Optional[str] = None
    number: Optional[int] = None

    is_designed: Optional[bool] = None

    json_sizes_box: Optional[Dict[str, Any]] = None


class CreateShelf(BaseModel):
    width: int
    length: int

    heigth: int
    margin_top: int
    margin_bottom: int

    poulticle_id: int


class UpdateShelf(BaseModel):
    width: Optional[int] = None
    length: Optional[int] = None

    heigth: Optional[int] = None
    margin_top: Optional[int] = None
    margin_bottom: Optional[int] = None

    json_shelf: Optional[Dict[str, Any]] = None
    json_rows: Optional[List[Dict[Any, Any]]] = None


class CreatePrepType(BaseModel):
    name: str


class CreatePackagingType(BaseModel):
    name: str

    front_svg: str
    side_svg: str
    top_svg: str


class UpdatePackagingType(BaseModel):
    name: Optional[str] = None

    front_svg: Optional[str] = None
    side_svg: Optional[str] = None
    top_svg: Optional[str] = None



class ProductCategory(BaseModel):
    name: str


class CreateProduct(BaseModel):
    name: str
    barcode: str
    client_id: int
    category_id: int=None
    packaging_type_id: int=None
    units_per_package: int
    size_1: float
    size_2: float
    size_3: float
    weight: float
    volume: float

    packaging_x: float
    packaging_y: float
    packaging_z: float

    packaging_obj: str

    facing_preview: str


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    barcode: Optional[str] = None
    units_per_package: Optional[int] = None
    size_1: Optional[float] = None
    size_2: Optional[float] = None
    size_3: Optional[float] = None
    weight: Optional[float] = None
    volume: Optional[float] = None

    packaging_x: float =0
    packaging_y: float=0
    packaging_z: float=0
    category_id:int = None
    packaging_obj: str
    packaging_type_id: int=None
    facing_preview: Optional[str] = None


class CreateProductOnShelf(BaseModel):
    shelf_id: int
    product_id: int
