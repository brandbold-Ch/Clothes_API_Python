from fastapi import FastAPI
from fastapi.responses import JSONResponse
from models.attributes import *
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional

# --------------------------------Star app--------------------------------------

root = FastAPI()

# -------------------------------Constantes de uso común------------------------

CONSTANTS = [
    JSONResponse(status_code=200, content={"message": "Success"}),
    JSONResponse(status_code=500, content={"message": "Unknown error"}),
    JSONResponse(status_code=200, content={"message": "Success added"}),
    JSONResponse(status_code=500, content={"message": "Unknown product"}),
    JSONResponse(status_code=500, content={"message": "Unknown branch"})
]


async def GET_JSON_DB(id: str) -> dict | JSONResponse:
    try:
        db = connection_primary()
        data = await db.table.find_one({"_id": ObjectId(id)})

        if data is None:
            return CONSTANTS[4]
        else:
            data["_id"] = str(data["_id"])
            return data
    except:
        return CONSTANTS[1]


# ------------------------------Conexión a la DB------------------------------

def connection_primary() -> motor:
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["sections"]
    return db


# ----------------------Método general para insertar datos a la db----------------

async def insert(table, database: motor) -> JSONResponse:
    try:
        await database.table.insert_one(jsonable_encoder(table))
        return CONSTANTS[2]
    except:
        return CONSTANTS[1]


# ----------------------------Método crear nueva sucursal--------------------------

@root.post("/new_branch")
async def new_branch(data: Clothing_Store):
    return await insert(table=data, database=connection_primary())


# --------------------------------Métodos POST de productos--------------------------

@root.post("/branch/{id}/t_shirts/person/{person}")
async def set_t_shirts(t_shirts: T_Shirts, id: str, person: str, identify="t_shirts"):
    return await put_products(data=t_shirts, branch=id, usage=person, keygen=identify)


@root.post("/branch/{id}/shorts/person/{person}")
async def set_shorts(shorts: Shorts, id: str, person: str, identify="shorts"):
    return await put_products(data=shorts, branch=id, usage=person, keygen=identify)


@root.post("/branch/{id}/shirts/person/{person}")
async def set_shirts(shirts: Shirts, id: str, person: str, identify="shirts"):
    return await put_products(data=shirts, branch=id, usage=person, keygen=identify)


@root.post("/branch/{id}/pants/person/{person}")
async def set_pants(pants: Pants, id: str, person: str, identify="pants"):
    return await put_products(data=pants, branch=id, usage=person, keygen=identify)


@root.post("/branch/{id}/shoes/person/{person}")
async def set_shoes(shoes: Shoes, id: str, person: str, identify="shoes"):
    return await put_products(data=shoes, branch=id, usage=person, keygen=identify)


@root.post("/branch/{id}/dresses/person/{person}")
async def set_dresses(dresses: Dresses, id: str, person: str, identify="dresses"):
    return await put_products(data=dresses, branch=id, usage=person, keygen=identify)


@root.post("/branch/{id}/footwear/person/{person}")
async def set_footwear(footwear: Footwear, id: str, person: str, identify="footwear"):
    return await put_products(data=footwear, branch=id, usage=person, keygen=identify)


# ----------------------------Agregar datos Inventario--------------------------

async def put_products(data, branch: str, usage: str, keygen: str) -> JSONResponse:
    try:
        db = connection_primary()
        path = usage + "." + keygen
        db.table.update_one({"_id": ObjectId(branch)}, {"$push": {path: jsonable_encoder(data)}})
        return CONSTANTS[2]
    except:
        return CONSTANTS[1]


@root.put("/branch/{id}/")
async def change_info(id: str, ID: str, t_shirts: T_Shirts):
    db = connection_primary()
    info = db.table.update_one({"_id": ObjectId(id)}, {"ID": "string"}, {"$set": {"women.t_shirts": jsonable_encoder(t_shirts)}})
    print(info)

# ----------------------------Obtener datos de una Sucursal---------------------------

@root.get("/branch/{id}")
async def get_branch(id: str, person: Optional[str] = None, product: Optional[str] = None):
    info = await GET_JSON_DB(id=id)

    if person is None and product is None:
        return info

    elif person is not None and product is None:
        return {person: info[person]}

    elif person is not None and product is not None:
        return {person: info[person][product]}
