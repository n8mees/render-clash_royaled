from bd.conexion import crBD
from bd.modelos.modelos import Carta, UpdateCarta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#pip install fastapi[all]
#pip install pymongo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Dominio de tu app React
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todas las cabeceras
)

def getCartas():
    data = crBD.find()
    arreglo = []
    for x in data:
        x["_id"] = str(x["_id"])
        arreglo.append(x)
    return arreglo

def existCarta(nombre: str):
    data = getCartas()
    existe = {}
    for x in data:
        if x["nombre"] == nombre:
            existe.update(x)
    return existe

@app.post("/Carta")
async def addCard(carta: Carta):
    existe = existCarta(carta.nombre)
    if not existe:
        crBD.insert_one(dict(carta))
        return {'detalle': dict(carta)}
    else:
        return {'detalle': 'Esta carta ya existe'}

@app.get("/Carta")
async def cards():
    data = getCartas()
    return data

@app.get("/Carta/{nombre}")
async def infoCarta(nombre: str):
    existe = existCarta(nombre)
    if not existe:
        return {'detalle': 'Esta carta no existe'}
    else:
        return {'detalle': existe}

@app.delete("/Carta/{nombre}")
async def deleteCard(nombre: str):
    existe = existCarta(nombre)
    if not existe:
        return {'detalle': 'Esta carta no existe'}
    else:
        crBD.find_one_and_delete({"nombre": nombre})
        return {'detalle': 'Esta carta ha sido eliminada'}

@app.patch("/Carta/{nombre}")
async def updateCarta(nombre: str, updateCarta: UpdateCarta):
    existe = existCarta(nombre)
    if not existe:
        return {'detalle': 'Esta carta no existe'}
    else:
        update_data = {k: v for k, v in updateCarta.dict().items() if v is not None}
        if not update_data:
            return {"status_code":400, "detail":"No se proporcionaron datos para actualizar"}
        crBD.update_one({"nombre": nombre}, {"$set": update_data})
        return {"detalle": "Esta carta ha sido actualizada"}
