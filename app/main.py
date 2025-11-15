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

# Configuration for Docker Containerization
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
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
# Database Path Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/data/database.db")
sqlite_url       = f"sqlite:///{DATABASE_PATH}"
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)

# Create Database File
def create_db_and_tables():
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
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
    return {
        "message": "Hello World!",
        "database_path": DATABASE_PATH
    }

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
@app.delete("/zones/{id}", status_code=204)
async def read_zone(id: int, session: SessionDep):
    data = session.get(Zone, id)
    if not data:
        raise HTTPException(status_code=404)
    session.delete(data)
    session.commit()