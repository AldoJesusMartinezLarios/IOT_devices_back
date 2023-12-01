import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Conecta a la base de datos
conn = sqlite3.connect("sql/dispositivos.db")

app = fastapi.FastAPI()

# Permitimos los origenes para conectarse
origins = [
    "http://0.0.0.0:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://wokwi.com/projects/382924417699279873",
    "https://iotfrontend-76a7ab26b9a7.herokuapp.com"
]

# Agregamos las opciones de origenes, credenciales, métodos y headers
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class Dispositivo(BaseModel):
    dispositivo: str
    valor: int

@app.post("/iot")
async def crear_dispositivo(dispositivo: Dispositivo):
    """Crea un nuevo dispositivo."""
    c = conn.cursor()
    c.execute('INSERT INTO iot (dispositivo, valor) VALUES (?, ?)',
              (dispositivo.dispositivo, dispositivo.valor))
    conn.commit()
    new_dispositivo_id = c.lastrowid  # Obtén el ID generado automáticamente
    return {"id": new_dispositivo_id, "dispositivo": dispositivo.dispositivo, "valor": dispositivo.valor}


@app.get("/iot")
async def obtener_dispositivos():
    """Obtiene todos los dispositivos."""
    c = conn.cursor()
    c.execute('SELECT * FROM iot')
    dispositivos = []
    for row in c.fetchall():
        dispositivo = {"id": row[0], "dispositivo": row[1], "valor": row[2]}
        dispositivos.append(dispositivo)
    return dispositivos

@app.get("/iot/{id}")
async def obtener_dispositivo(id: int):
    """Obtiene un dispositivo por su ID."""
    c = conn.cursor()
    c.execute('SELECT * FROM iot WHERE id = ?', (id,))
    row = c.fetchone()
    if row:
        dispositivo = {"id": row[0], "dispositivo": row[1], "valor": row[2]}
        return dispositivo
    else:
        return {"error": -1}

@app.patch("/iot/{id}/{valor}")
async def actualizar_dispositivo(id: int, valor: int):
    """Actualiza el valor de un dispositivo."""
    # Verifica si el dispositivo existe antes de actualizar
    c = conn.cursor()
    c.execute('SELECT * FROM iot WHERE id = ?', (id,))
    row = c.fetchone()
    if not row:
        return {"error": -1}

    # Actualiza el valor del dispositivo en la base de datos
    c.execute('UPDATE iot SET valor = ? WHERE id = ?', (valor, id))
    conn.commit()

    # Retorna el resultado
    return {"valor": valor}

@app.delete("/iot/{id}")
async def eliminar_dispositivo(id: int):
    """Elimina un dispositivo."""
    c = conn.cursor()
    c.execute('DELETE FROM iot WHERE id = ?', (id,))
    conn.commit()
    return {"message": "Dispositivo eliminado"}