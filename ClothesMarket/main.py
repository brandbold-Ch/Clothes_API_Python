from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from models.attributes import *
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, Dict, Any, Union, List


# --------------------------------Star app--------------------------------------

root = FastAPI()

# -------------------------------Constantes de uso común------------------------

CONSTANTS = [
    JSONResponse(status_code=200, content={"message": "Success"}),
    JSONResponse(status_code=500, content={"message": "Unknown error"}),
    JSONResponse(status_code=200, content={"message": "Success added"}),
    JSONResponse(status_code=400, content={"message": "Unknown product"})
]


async def GET_JSON_DB(id: str) -> list[Any] | JSONResponse:
    try:
        db = connection_primary()
        data = await db.table.find_one({"_id": ObjectId(id)})
        data["_id"] = str(data["_id"])
        return data
    except Exception as e:
        print(e)
        return CONSTANTS[1]


# ------------------------------Conexión a la DB------------------------------

def connection_primary() -> motor:
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["sections"]
    return db


# ----------------------Método general para insertar datos a la db----------------

async def insert(table, database) -> JSONResponse:
    try:
        await database.table.insert_one(jsonable_encoder(table))
        return CONSTANTS[0]
    except:
        return CONSTANTS[2]


# ----------------------------Método crear nueva tienda----------------------------

@root.post("/new_branch")
async def new_branch(data: Clothing_Store):
    return await insert(table=data, database=connection_primary())


# --------------------------------Métodos POST de productos--------------------------

@root.post("/branch/{id}/t_shirts")
async def set_t_shirts(t_shirts: T_Shirts, id: str):
    return await put_set_products(array=t_shirts, branch=id)


@root.post("branch/{id}/shorts")
async def set_shorts(shorts: Shorts, id: str):
    return await put_set_products(array=shorts, branch=id)


@root.post("/branch/{id}/shirts")
async def set_shirts(shirts: Shirts, id: str):
    return await put_set_products(array=shirts, branch=id)


@root.post("/branch/{id}/pants")
async def set_pants(pants: Pants, id: str):
    return await put_set_products(array=pants, branch=id)


@root.post("/branch/{id}/shoes")
async def set_shoes(shoes: Shoes, id: str):
    return await put_set_products(array=shoes, branch=id)


@root.post("/branch/{id}/dresses")
async def set_dresses(dresses: Dresses, id: str):
    return await put_set_products(array=dresses, branch=id)


@root.post("/branch/{id}/footwear")
async def set_footwear(footwear: Footwear, id: str):
    return await put_set_products(array=footwear, branch=id)


# ----------------------------Agregar datos PUT Inventario--------------------------

async def put_set_products(array, branch: str):
    try:
        db = connection_primary()
        cursor = db.table.find({"_id": ObjectId(branch), "women": {"$exists": True}})
        db.table.update_one({"_id": ObjectId(branch)}, {"$push": {"women.t_shirts": jsonable_encoder(array)}})
    except Exception as e:
        print(e)
        return True


# ----------------------------Obtener datos Inventario-------------------------------

@root.get("/products/branch{id}/")
async def get_products():
    try:
        db = GET_JSON_DB(id)
    except:
        return CONSTANTS[1]
