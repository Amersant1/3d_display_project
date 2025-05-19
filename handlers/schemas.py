from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Json
from pydantic import field_validator
from pydantic.dataclasses import dataclass
from typing import Optional, List, Any,Dict,Union


class RunSequence(BaseModel):
    l: List[str]


class CreateEmployee(BaseModel):
    full_name: str


class UpdateEmployee(BaseModel):
    full_name: str

    created: Optional[datetime] = None


class CreateClient(BaseModel):
    name: str


class UpdateClient(BaseModel):
    name: str

    created: Optional[datetime] = None


class Copy(BaseModel):
    id:int = 0


class AddProject(BaseModel):
    name: str
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    number :Optional[str] = None
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
    number : Optional[str] = None
    created: Optional[datetime] = None


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
    number: str

    json_sizes_box: Optional[Dict[str, Any]] = {"width": 100, "height": 100, "depth": 100}

    number_of_shelves: Optional[int] = 4
    width_mm: Optional[float] = 380
    depth_mm: Optional[float] = 280
    sides_height_mm: Optional[float] = 1320
    sides_width_mm: Optional[float] = 17
    back_width_mm: Optional[float] = 10
    front_width_mm: Optional[float] = 25
    shelf_width_mm: Optional[float] = 20
    fronton_height_mm: Optional[float] = 200
    topper_height_mm: Optional[float] = 0


class UpdatePoultice(BaseModel):
    project_id: Optional[int] = None
    file: Optional[str] = None
    type_id: Optional[int] = None
    size_x: Optional[float] = None
    size_y: Optional[float] = None
    size_z: Optional[float] = None

    name: Optional[str] = None
    image: Optional[str] = None
    number: Optional[str] = None

    is_designed: Optional[bool] = None

    json_sizes_box: Optional[Dict[str, Any]] = None

    number_of_shelves: Optional[int] = None
    width_mm: Optional[float] = None
    depth_mm: Optional[float] = None
    sides_height_mm: Optional[float] = None
    sides_width_mm: Optional[float] = None
    back_width_mm: Optional[float] = None
    front_width_mm: Optional[float] = None
    shelf_width_mm: Optional[float] = None
    fronton_height_mm: Optional[float] = None
    topper_height_mm: Optional[float] = None

    created: Optional[datetime] = None


class CreateShelf(BaseModel):
    width: int
    length: int

    heigth: int
    margin_top: int
    margin_bottom: int

    poulticle_id: int

    isRows: Optional[bool] = True


class UpdateShelf(BaseModel):
    width: Optional[int] = None
    length: Optional[int] = None

    heigth: Optional[int] = None
    margin_top: Optional[int] = None
    margin_bottom: Optional[int] = None

    json_shelf: Optional[Dict[str, Any]] = None
    json_rows: Union[dict, list] = None
    active : bool = None

    isRows: bool = False

    created: Optional[datetime] = None


class CreatePrepType(BaseModel):
    name: str


class UpdatePrepType(BaseModel):
    name: str

    created: Optional[datetime] = None


class CreatePackagingType(BaseModel):
    name: str

    front_svg: str
    side_svg: Optional[str] = None
    top_svg: str

    object: Optional[str] = None


class UpdatePackagingType(BaseModel):
    name: Optional[str] = None
    front_svg: Optional[str] = None
    side_svg: Optional[str] = None
    top_svg: Optional[str] = None
    object: Optional[str] = None
    created: Optional[datetime] = None


class ProductCategory(BaseModel):
    name: str


class UpdateProductCategory(BaseModel):
    name: str

    created: Optional[datetime] = None


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

    created: Optional[datetime] = None


class CreateProductOnShelf(BaseModel):
    shelf_id: int
    product_id: int
