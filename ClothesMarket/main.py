import starlette.middleware.base
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from models.attributes import *
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from typing import Optional, Any, Dict
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# --------------------------------Star app--------------------------------------

root = FastAPI()


# templates = Jinja2Templates(directory="templates")
# root.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------Middleware's-----------------------------------

@root.middleware("http")
async def my_middleware(request: Request, call_next) -> starlette.middleware.base.StreamingResponse:
    print(f"Accediendo a {request.url}")
    response = await call_next(request)
    return response


# --------------------------------------Authentication-----------------------------

def authentication(request: Request) -> None:
    pass


# -------------------------------Método para obtener datos de la DB-----------------


async def GET_JSON_DB(id: str) -> dict | JSONResponse:
    try:
        db = connection_primary()
        data = await db.table.find_one({"_id": ObjectId(id)})

        if data is None:
            return JSONResponse(status_code=404, content={"message": "Unknown branch"})
        else:
            data["_id"] = str(data["_id"])
            return data

    except Exception as error:
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ------------------------------Conexión a la DB------------------------------

def connection_primary() -> motor.motor_asyncio.AsyncIOMotorClient:
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://223031:EWwe05ZQcQgV9AuR@cluster0.glnagiz.mongodb.net/?retryWrites=true&w=majority")
    db = client["sections"]
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
async def set_t_shirts(t_shirts: T_Shirts, id: str, person: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=id, usage=person, keygen="t_shirts")


@root.post("/branch/{id}/shorts/{person}")
async def set_shorts(shorts: Shorts, id: str, person: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=id, usage=person, keygen="shorts")


@root.post("/branch/{id}/shirts/{person}")
async def set_shirts(shirts: Shirts, id: str, person: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=id, usage=person, keygen="shirts")


@root.post("/branch/{id}/pants/{person}")
async def set_pants(pants: Pants, id: str, person: str) -> JSONResponse:
    return await insert_products(data=pants, branch=id, usage=person, keygen="pants")


@root.post("/branch/{id}/shoes/{person}")
async def set_shoes(shoes: Shoes, id: str, person: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=id, usage=person, keygen="shoes")


@root.post("/branch/{id}/dresses/{person}")
async def set_dresses(dresses: Dresses, id: str, person: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=id, usage=person, keygen="dresses")


@root.post("/branch/{id}/footwear/{person}")
async def set_footwear(footwear: Footwear, id: str, person: str) -> JSONResponse:
    return await insert_products(data=footwear, branch=id, usage=person, keygen="footwear")


# ----------------------------Métodos PUT para modificar datos-----------------

@root.put("/branch/{id}/t_shirts/{person}/{index}")
async def put_t_shirts(t_shirts: T_Shirts, id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=id, usage=person, keygen="t_shirts", index=index)


@root.put("/branch/{id}/shorts/{person}/{index}")
async def put_shorts(shorts: Shorts, id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=id, usage=person, keygen="shorts", index=index)


@root.put("/branch/{id}/shirts/{person}/{index}")
async def set_shirts(shirts: Shirts, id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=id, usage=person, keygen="shirts", index=index)


@root.put("/branch/{id}/pants/{person}/{index}")
async def set_pants(pants: Pants, id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=pants, branch=id, usage=person, keygen="pants", index=index)


@root.put("/branch/{id}/shoes/{person}/{index}")
async def set_shoes(shoes: Shoes, id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=id, usage=person, keygen="shoes", index=index)


@root.put("/branch/{id}/dresses/{person}/{index}")
async def set_dresses(dresses: Dresses, id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=id, usage=person, keygen="dresses", index=index)


@root.put("/branch/{id}/footwear/{person}/{index}")
async def set_footwear(footwear: Footwear, id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=footwear, branch=id, usage=person, keygen="footwear", index=index)


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

@root.get("/branch/{id}")
async def get_branch(id: str, person: Optional[str] = None, product: Optional[str] = None) -> JSONResponse:
    info = await GET_JSON_DB(id=id)

    try:
        if person is None and product is None:
            return JSONResponse(status_code=200, content={"branch": info})

        elif person is not None and product is None:
            return JSONResponse(status_code=200, content={person: info[person]})

        elif person is not None and product is not None:
            return JSONResponse(status_code=200, content={person: info[person][product]})
    except:
        return JSONResponse(status_code=500, content={"message": "Unknown error"})

