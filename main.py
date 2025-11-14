'''
Development TIPS
 
 - Preliminary Setup (Linux):
    In Terminal:
        - mkdir <projectName>
        - cd <projectName>
        - python3 -m venv .venv
        - . .\.venv\bin\activate
        - echo ".venv" > .gitignore
        - pip install --upgrade pip
        - pip install "fastapi[standard]"
        - pip freeze > requirements.txt
        - git init
        - git add .
        - git commit -m "initial commit"
        - touch main.py
        - code .

- Preliminary Setup (Windows):
    In Terminal:
        - mkdir <projectName>
        - cd <projectName>
        - python3 -m venv .venv
        - .\venv\Scripts\activate
        - echo ".venv" > .gitignore # (remove "" later in the file)
        -  python.exe -m pip install --upgrade pip
        - pip install "fastapi[standard]"
        - pip freeze > requirements.txt
        - git init
        - git add .
        - git commit -m "initial commit"
        - type nul > main.py
        - code . 
        
 
 - In settings (top bar --> >Preferences User Settings (json)) add:
    "python.analysis.typeCheckingMode": "strict"

 - Add Pylance and Python extensions
 - Open .venv on terminal:
    - Terminal --> new Terminal
    - In Terminal (Windown) --> .venv\Scripts\activate
    - In Terminal (Linux)   --> . .\.venv\bin\activate
 - To run code (in (.venv) terminal):
    fastapi dev main.py

'''

'''
Data Schema

Zones
 - zone_id
 - name
 - region
 - created_at

Measure
 - measure_id
 - device_id
 - name
 - value
 - due_date
 - created_at

Device
 - device_id
 - zone_id
 - name
'''

### Modules Importation ###

from contextlib import asynccontextmanager
from random import randint
# Import the FastAPI framework
from fastapi import Depends, FastAPI, HTTPException, Response
from datetime import datetime, timezone
from typing import Annotated, Generic, TypeVar
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Session, create_engine, select

### Data Crafting ###

# Zones Table
class Zone(SQLModel, table=True):
    zone_id:    int | None = Field(default=None, primary_key=True)
    name:       str =        Field(index=True)
    region:     str | None = Field(default=None, index=True)
    created_at: datetime   = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)

# Zone Blueprint for POST operations
class ZoneCreate(SQLModel):
    name:   str = Field(index=True)
    region: str = Field(default=None, index=True)


### Database Startup and Setup ###

sqlite_file_name = "database.db"
sqlite_url       = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)

# Create Database File
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Get session from the engine
def get_session():
    with Session(engine) as session:
        yield session
    
SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
       if not session.exec(select(Zone)).first():
           session.add_all([
               Zone(name="Milan", region="Italy North"),
               Zone(name="Rome", region="Italy Center")
           ])
           session.commit()
    yield

### Application Creation ###


# define app as a FastAPI instance
# define /api/v1 as application root point
app = FastAPI(root_path="/api/v1", lifespan=lifespan)

# decorator --> associate web page to a certain function
# name.method(PATH)
@app.get("/")
async def root():
    return {"message": "Hello World!"}

# Generic class to not create a class for every endpoint
T = TypeVar("T")
class Response(BaseModel, Generic[T]):
    data: T

# zones getter
# response model to make documentation better
@app.get("/zones", response_model=Response[list[Zone]])
async def read_zones(session: SessionDep):
    data = session.exec(select(Zone)).all()
    return {"data": data}

# specific zone getter
@app.get("/zones/{id}", response_model=Response[Zone])
async def read_zone(id: int, session: SessionDep):
    data = session.get(Zone, id)
    if not data:
        raise HTTPException(status_code=404)
    return {"data": data}

# zone creator
@app.post("/zones/{id}", status_code=201, response_model=Response[Zone])
async def create_zone(zone: ZoneCreate, session: SessionDep):
    # validate our zone against the actual table class
    db_zone = Zone.model_validate(zone)
    session.add(db_zone)
    session.commit()
    session.refresh(db_zone)
    return {"data": db_zone}

# zone updater
@app.put("/zones/{id}", response_model=Response[Zone])
async def update_zone(id: int, zone: ZoneCreate, session: SessionDep):
    data = session.get(Zone, id)
    if not data:
        raise HTTPException(status_code=404)
    data.name    = zone.name
    data.region = zone.region
    session.add(data)
    session.commit()
    session.refresh(data)
    return {"data": data}

# zone deleter
@app.delete("zones/{id}", status_code=204)
async def delete_zone(id: int, session: SessionDep):
    data = session.get(Zone, id)
    if not data:
        raise HTTPException(status_code=404)
    session.delete(data)
    session.commit()

#### NO DATABASE CODE ####
# data : Any = [
#     {
#         "zone_id": 1,
#         "name": "Milan",
#         "region": "North Italy",
#         "created_at": datetime.now()
#     },
#     {
#         "zone_id": 2,
#         "name": "Bergamo",
#         "region": "North Italy",
#         "created_at": datetime.now()
#     }
# ]
# 
# # zones getter
# @app.get("/zones")
# async def read_zones():
#     return {"zones": data}
# 
# # specific zone get
# @app.get("/zones/{id}")
# async def read_zone(id:int):
#     for zone in data:
#         if zone.get("zone_id") == id:
#             return {"campaign": zone}
#     raise HTTPException(status_code=404)
# 
# # post zone --> add a new zone
# @app.post("/zones", status_code=201)
# async def create_zone(body : dict[str, Any]):
# 
#     new : Any = { 
#         "zone_id": randint(100, 1000),
#         "name": body.get("name"), 
#         "region": body.get("region"),
#         "created_at": datetime.now()
#     }
# 
#     data.append(new)
#     return {"zone": new}
# 
# # put zone --> update zone
# @app.put("/zones/{id}")
# async def update_campaing(id: int, body: dict[str, Any]):
# 
#     for index, zone in enumerate(data):
#         if zone.get("zone_id") == id:
#             updated : Any = { 
#                 "zone_id": id,
#                 "name": body.get("name"), 
#                 "region": body.get("region"),
#                 "created_at": zone.get("created_at")
#             }
# 
#             data[index] = updated
#             return {"zone": updated}
#     raise HTTPException(status_code=404)
# 
# # delete zone
# @app.delete("/zones/{id}")
# async def update_campaing(id: int, body: dict[str, Any]):
# 
#     for index, zone in enumerate(data):
#         if zone.get("zone_id") == id:
#             data.pop(index)
#             return Response(status_code=204)
#     raise HTTPException(status_code=404)