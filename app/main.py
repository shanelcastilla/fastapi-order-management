from fastapi import FastAPI
from sqlalchemy import text
from app.databases.connection import engine

from app.routes import users, product, order

app = FastAPI(
     title="Order API",
     version="1.0.0"
)

app.include_router(users.router)
app.include_router(product.router)
app.include_router(order.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando",
        "message": "API working",
        "status": "ok",
        "estado": "correcto"
    }


# @app.get("/hola")
# def usuerio ():
#       return "hola"


@app.get("/get_db")
def conexion():
   with engine.connect() as conexion:
        result = conexion.execute(text("SELECT 1"))

   return {
        "databases" : "connected",
        "result" : result.scalar()
        
   }
   
