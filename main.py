'''
Development TIPS
 - In settings (top bar --> >Preferences User Settings (json)) add:
"python.analysis.typeCheckingMode": "strict"

 - Add Pylance and Python extensions

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

# Import the FastAPI framework
from random import randint
from fastapi import FastAPI, HTTPException, Request, Response
from datetime import datetime
from typing import Any


# define app as a FastAPI instance
# define /api/v1 as application root point
app = FastAPI(root_path="/api/v1")

# decorator --> associate web page to a certain function
# name.method(PATH)
@app.get("/")
async def root():
    return {"message": "Hello World!"}

data : Any = [
    {
        "zone_id": 1,
        "name": "Milan",
        "region": "North Italy",
        "created_at": datetime.now()
    },
    {
        "zone_id": 2,
        "name": "Bergamo",
        "region": "North Italy",
        "created_at": datetime.now()
    }
]

# zones getter
@app.get("/zones")
async def read_zones():
    return {"zones": data}

# specific zone get
@app.get("/zones/{id}")
async def read_zone(id:int):
    for zone in data:
        if zone.get("zone_id") == id:
            return {"campaign": zone}
    raise HTTPException(status_code=404)

# post zone --> add a new zone
@app.post("/zones", status_code=201)
async def create_zone(body : dict[str, Any]):

    new : Any = { 
        "zone_id": randint(100, 1000),
        "name": body.get("name"), 
        "region": body.get("region"),
        "created_at": datetime.now()
    }

    data.append(new)
    return {"zone": new}

# put zone --> update zone
@app.put("/zones/{id}")
async def update_campaing(id: int, body: dict[str, Any]):

    for index, zone in enumerate(data):
        if zone.get("zone_id") == id:
            updated : Any = { 
                "zone_id": id,
                "name": body.get("name"), 
                "region": body.get("region"),
                "created_at": zone.get("created_at")
            }

            data[index] = updated
            return {"zone": updated}
    raise HTTPException(status_code=404)

# delete zone
@app.delete("/zones/{id}")
async def update_campaing(id: int, body: dict[str, Any]):

    for index, zone in enumerate(data):
        if zone.get("zone_id") == id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404)