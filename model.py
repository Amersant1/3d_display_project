from datetime import datetime

from controller import *

from sqlalchemy import *
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.mutable import MutableDict,MutableList


Base = declarative_base()


class Client(Base):
    """
    Таблица: Клиенты (Clients)
    
    Поля:
    - id: Числовой (Зн.), код клиента (Primary Key)
    - name: Симв. (64 зн.), название клиента
    """
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    active = Column(Boolean, default=True)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)


class ProductCategory(Base):
    """
    Таблица: Категория продукта (Product Category)
    
    Поля:
    - id: Числовой (Зн.), код категории (Primary Key)
    - name: Симв. (64 зн.), название категории
    """
    __tablename__ = 'product_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    active = Column(Boolean, default=True)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)


class PackagingType(Base):
    """
    Таблица: Вид упаковки (Packaging Type)
    
    Поля:
    - id: Числовой (Зн.), код вида упаковки (Primary Key)
    - name: Симв. (64 зн.), название вида упаковки
    
    Возможные значения:
    - 1: Овал/Blister
    - 2: Короб
    - 3: Спичечный (?)
    - 4: Подвесной
    - 5: Накопочный короб
    """
    __tablename__ = 'packaging_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    front_svg = Column(String(64))
    side_svg = Column(String(64))
    top_svg = Column(String(64))

    active = Column(Boolean, default=True)

    object = Column(String(64))

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)


class PrepType(Base):
    """
    Таблица: Тип препака (Prep Type)
    
    Поля:
    - id: Числовой (Зн.), код типа препака (Primary Key)
    - name: Симв. (64 зн.), название типа препака
    
    Возможные значения:
    - 1/4 напольный патент
    - 1/4 напольный эконом
    - 1/4 напольный на держателях
    - 1/4 напольный обейджик
    - 1/8 напольный патент
    - 1/8 напольный эконом
    - 1/8 напольный на держателях
    - 1/8 напольный обейджик
    - Подвесной
    """
    __tablename__ = 'prep_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

    active = Column(Boolean, default=True)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)


class Employee(Base):
    """
    Таблица: Сотрудники (Employees)
    
    Поля:
    - id: Числовой (Зн.), код сотрудника (Primary Key)
    - full_name: Симв. (128 зн.), ФИО
    """
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(128))

    active = Column(Boolean, default=True)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)


class Product(Base):
    """
    Таблица: Продукты (Products)
    
    Поля:
    - id: Числовой (Зн.), код продукта (Primary Key)
    - name: Симв. (64 зн.), название продукта
    - barcode: Симв. (64 зн.), штрих-код продукта
    - client_id: Числовой (Зн.), код клиента (Foreign Key)
    - category_id: Числовой (Зн.), код категории продукта (Foreign Key)
    - packaging_type_id: Числовой (Зн.), код вида упаковки (Foreign Key)
    - units_per_package: Числовой (Зн.), количество единиц продукта в 1й упаковке
    - size_1: Числовой (Зн.), размер 1 в мм
    - size_2: Числовой (Зн.), размер 2 в мм
    - size_3: Числовой (Зн.), размер 3 в мм
    - weight: Числовой (Зн.), вес 1 упаковки в граммах
    - volume: Числовой (Зн.), объем 1 упаковки
    - facing_preview: Симв. (64 зн.), превью фейсинга (путь к JPG файлу)
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    barcode = Column(String(64))
    client_id = Column(Integer, ForeignKey('clients.id'))
    category_id = Column(Integer, ForeignKey('product_categories.id'))
    packaging_type_id = Column(Integer, ForeignKey('packaging_types.id'))
    units_per_package = Column(Integer)
    size_1 = Column(Float)
    size_2 = Column(Float)
    size_3 = Column(Float)
    weight = Column(Float)
    volume = Column(Float)
    facing_preview = Column(String(64))  # Assuming this is a filepath to the image

    packaging_x = Column(Float)
    packaging_y = Column(Float)
    packaging_z = Column(Float)

    packaging_obj = Column(String(64))

    client = relationship('Client')
    category = relationship('ProductCategory', lazy="selectin")
    packaging_type = relationship('PackagingType', lazy="selectin")

    active = Column(Boolean, default=True)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)

class Project(Base):
    __tablename__="projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client')
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee')
    number = Column(Integer,default = 0)
    active = Column(Boolean, default=True)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)

class Poultice(Base):
    """Припак
    название
    """
    __tablename__="poultices"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project')
    file = Column(String(1000))
    type_id = Column(Integer, ForeignKey('prep_types.id'))  # Foreign key to prep_types

    name = Column(String(128))
    image = Column(String(256))
    number = Column(Integer)

    size_x = Column(Float)
    size_y = Column(Float)
    size_z = Column(Float)

    is_designed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    type = relationship('PrepType', lazy="selectin")
    shelves = relationship('Shelf', back_populates="poulticle")

    active = Column(Boolean, default=True)

    json_sizes_box = Column(MutableDict.as_mutable(JSON), default=lambda: {})

    number_of_shelves = Column(Integer)
    width_mm = Column(Float)
    depth_mm = Column(Float)
    sides_height_mm = Column(Float)
    sides_width_mm = Column(Float)
    back_width_mm = Column(Float)
    front_width_mm = Column(Float)
    shelf_width_mm = Column(Float)
    fronton_height_mm = Column(Float)
    topper_height_mm = Column(Float)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)

    original_id = Column(Integer, default=0)
    session_name = Column(String(32), default="")


class Shelf(Base):
    """
    Таблица: Полки (Shelves)
    
    Поля:
    - id: Числовой (Зн.), код полки (Primary Key)
    products = 

    """
    __tablename__="shelves"
    id = Column(Integer, primary_key=True)
    width = Column(Integer)
    length = Column(Integer)

    json_shelf = Column(MutableDict.as_mutable(JSON), default=lambda: {})
    json_rows = Column(MutableDict.as_mutable(JSON), default=lambda:  {})

    heigth = Column(Integer)
    margin_top = Column(Integer)
    margin_bottom = Column(Integer)
    poulticle_id = Column(Integer,ForeignKey('poultices.id'))
    poulticle = relationship("Poultice",back_populates="shelves")

    active = Column(Boolean, default=True)

    isRows = Column(Boolean, default=True)

    created = Column(DateTime, default=datetime.now)
    last_updated = Column(DateTime, default=datetime.now)

    original_id = Column(Integer, default=0)
    session_name = Column(String(32), default="")

# class ProductOnShelf(Base):
#     __tablename__ = "products_on_shelves"
#     id = Column(Integer, primary_key=True)
#     shelf_id = Column(Integer, ForeignKey('shelves.id'))
#     product_id = Column(Integer, ForeignKey('products.id'))
#     shelf = relationship('Shelf')
#     product = relationship('Product', lazy="selectin")


async def make_session() -> AsyncSession:
    async with Session() as session:
        yield session



# Подключение к базе данных
# Base.metadata.create_all(engine)
