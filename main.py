import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Crea la base de datos
conn = sqlite3.connect("sql/dispositivos.db")

app = fastapi.FastAPI()

origins = [
    "https://8080-aldojesusma-iotdevicesf-a4w6rsh4ddx.ws-us106.gitpod.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Dispositivo(BaseModel):
    id: int
    dispositivo: str
    valor: int

class DispositivoPUT(BaseModel):
    valor: int

@app.get("/")
async def root():
    return "Conexion exitosa"

@app.get("/dispositivos")
async def get_all():
    """Obtiene todos los dispositivos."""
    c = conn.cursor()
    c.execute('SELECT * FROM dispositivos;')
    response = []
    for row in c:
        dispositivo = {"id": row[0], "dispositivo": row[1], "valor": row[2]}
        response.append(dispositivo)
    return response

@app.get("/dispositivos/{id}")
async def get_dispositivo(id: int):
    """Obtiene un dispositivo por su id."""
    try:
        # Consulta el dispositivo por su id
        c = conn.cursor()
        c.execute('SELECT * FROM dispositivos WHERE id = ?', (id,))
        dispositivo = None
        for row in c:
            dispositivo = {"id": row[0], "dispositivo": row[1], "valor": row[2]}
        if dispositivo is not None:
            return dispositivo
        else:
            return fastapi.Response(content=f"Dispositivo con ID {id} no encontrado", status_code=-1)
    except Exception as e:
        # Manejar la excepción y devolver el código de respuesta -1
        return fastapi.Response(content=f"Error: {str(e)}", status_code=-1)


@app.put("/dispositivos/{id}")
async def put_dispositivo(id: int, dispositivo: DispositivoPUT):
    """Actualiza un dispositivo por su id."""
    try:
        # Actualiza un dispositivo por su id.
        c = conn.cursor()
        c.execute('UPDATE dispositivos SET valor = ? WHERE id = ?;', (dispositivo.valor, id))
        conn.commit()
        return dispositivo
    except Exception as e:
        # Manejar la excepción y devolver el código de respuesta -1
        return fastapi.Response(content=f"Error: {str(e)}", status_code=-1)
