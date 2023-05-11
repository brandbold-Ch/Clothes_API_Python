import motor.motor_asyncio
import starlette.middleware.base
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from models.models_products import *
from dotenv import load_dotenv
from typing import Optional
from bson import ObjectId
import os
import motor

# --------------------------------Star app--------------------------------------

root = FastAPI()


# -------------------------------Middleware's-----------------------------------

@root.middleware("http")
async def my_middleware(request: Request, call_next) -> starlette.middleware.base.StreamingResponse:
    print(f"Accediendo a {request.url}")
    response = await call_next(request)
    return response


# --------------------------------------Authentication-----------------------------

@root.get("/login/auth")
async def login(username: str = None, password: str = None):
    try:
        db = await get_users()
        access = db.users.find_one({})

        if access is not None:
            pass

    except Exception as error:
        print(error)
        return JSONResponse(status_code=404, content={"message": "User not found"})


# -------------------------------Método para obtener datos de la DB-----------------


async def GET_JSON_DB(_id: str) -> dict | JSONResponse:
    try:
        db = connection_primary()
        data = await db.table.find_one({"_id": ObjectId(_id)})

        if data is None:
            return JSONResponse(status_code=404, content={"message": "Unknown branch"})
        else:
            data["_id"] = str(data["_id"])
            return data

    except Exception as error:
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ------------------------------Conexión a la DB------------------------------

def connection_primary() -> motor.motor_asyncio.AsyncIOMotorClient:
    load_dotenv()
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client["sections"]
    return db


def get_users() -> motor.motor_asyncio.AsyncIOMotorClient:
    load_dotenv()
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client["users"]
    return db


# ----------------------Método para insertar datos a la db ------------------

async def insert(table, database: motor) -> JSONResponse:
    try:
        await database.table.insert_one(jsonable_encoder(table))
        return JSONResponse(status_code=201, content={"message": "Added branch"})

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ----------------------------Método crear nueva sucursal----------------------

@root.post("/new_branch")
async def new_branch(data: Clothing_Store) -> JSONResponse:
    return await insert(table=data, database=connection_primary())


# --------------------------------Métodos POST de productos-----------------------------

@root.post("/branch/{id}/t_shirts/{person}")
async def set_t_shirts(t_shirts: T_Shirts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=_id, usage=person, keygen="t_shirts")


@root.post("/branch/{id}/shorts/{person}")
async def set_shorts(shorts: Shorts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=_id, usage=person, keygen="shorts")


@root.post("/branch/{id}/shirts/{person}")
async def set_shirts(shirts: Shirts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=_id, usage=person, keygen="shirts")


@root.post("/branch/{id}/pants/{person}")
async def set_pants(pants: Pants, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=pants, branch=_id, usage=person, keygen="pants")


@root.post("/branch/{id}/shoes/{person}")
async def set_shoes(shoes: Shoes, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=_id, usage=person, keygen="shoes")


@root.post("/branch/{id}/dresses/{person}")
async def set_dresses(dresses: Dresses, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=_id, usage=person, keygen="dresses")


@root.post("/branch/{id}/footwear/{person}")
async def set_footwear(footwear: Footwear, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=footwear, branch=_id, usage=person, keygen="footwear")


# ----------------------------Métodos PUT para modificar datos-----------------

@root.put("/branch/{id}/t_shirts/{person}/{index}")
async def put_t_shirts(t_shirts: T_Shirts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=_id, usage=person, keygen="t_shirts", index=index)


@root.put("/branch/{id}/shorts/{person}/{index}")
async def put_shorts(shorts: Shorts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=_id, usage=person, keygen="shorts", index=index)


@root.put("/branch/{id}/shirts/{person}/{index}")
async def set_shirts(shirts: Shirts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=_id, usage=person, keygen="shirts", index=index)


@root.put("/branch/{id}/pants/{person}/{index}")
async def set_pants(pants: Pants, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=pants, branch=_id, usage=person, keygen="pants", index=index)


@root.put("/branch/{id}/shoes/{person}/{index}")
async def set_shoes(shoes: Shoes, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=_id, usage=person, keygen="shoes", index=index)


@root.put("/branch/{id}/dresses/{person}/{index}")
async def set_dresses(dresses: Dresses, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=_id, usage=person, keygen="dresses", index=index)


@root.put("/branch/{id}/footwear/{person}/{index}")
async def set_footwear(footwear: Footwear, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=footwear, branch=_id, usage=person, keygen="footwear", index=index)


# ----------------------------Agregar datos Inventario--------------------------

async def insert_products(data=None, branch: str = None, usage: str = None, keygen: str = None, index: str = None) -> JSONResponse:
    try:
        db = connection_primary()
        path_insert = f"{usage}.{keygen}"
        path_update = f"{usage}.{keygen}.{index}"

        if index is None:
            db.table.update_one({"_id": ObjectId(branch)}, {"$push": {path_insert: jsonable_encoder(data)}})
            return JSONResponse(status_code=201, content={"message": "Added information"})
        else:
            db.table.update_one({"_id": ObjectId(branch)}, {"$set": {path_update: jsonable_encoder(data)}})
            return JSONResponse(status_code=201, content={"message": "Added information"})

    except Exception as error:
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ----------------------------Obtener datos de una Sucursal con query's---------------------------

@root.get("/branch/{_id}")
async def get_branch(_id: str, person: Optional[str] = None, product: Optional[str] = None) -> JSONResponse:
    info = await GET_JSON_DB(_id=_id)

    try:
        if person is None and product is None:
            return JSONResponse(status_code=200, content={"branch": info})

        elif person is not None and product is None:
            return JSONResponse(status_code=200, content={person: info[person]})

        elif person is not None and product is not None:
            return JSONResponse(status_code=200, content={person: info[person][product]})

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})
