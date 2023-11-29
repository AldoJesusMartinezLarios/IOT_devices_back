import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Conecta a la base de datos
conn = sqlite3.connect("sql/devices.db")

app = fastapi.FastAPI()

origins = [
    "http://127.0.0.1:8080"  # Cambia la URL según tu frontend de dispositivos
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Device(BaseModel):
    device: str
    value: int

@app.post("/iot")
async def crear_dispositivo(device: Device):
    """Crea un nuevo dispositivo."""
    c = conn.cursor()
    c.execute('INSERT INTO iot (device, value) VALUES (?, ?)',
              (device.device, device.value))
    conn.commit()
    new_device_id = c.lastrowid  # Obtén el ID generado automáticamente
    return {"id": new_device_id, "device": device.device, "value": device.value}


@app.get("/iot")
async def obtener_dispositivos():
    """Obtiene todos los dispositivos."""
    c = conn.cursor()
    c.execute('SELECT * FROM iot')
    devices = []
    for row in c.fetchall():
        device = {"id": row[0], "device": row[1], "value": row[2]}
        devices.append(device)
    return devices

@app.get("/iot/{id}")
async def obtener_dispositivo(id: int):
    """Obtiene un dispositivo por su ID."""
    c = conn.cursor()
    c.execute('SELECT * FROM iot WHERE id = ?', (id,))
    row = c.fetchone()
    if row:
        device = {"id": row[0], "device": row[1], "value": row[2]}
        return device
    else:
        return {"error": -1}

@app.patch("/iot/{id}/{value}")
async def actualizar_dispositivo(id: int, value: int):
    """Actualiza el valor de un dispositivo."""
    # Verifica si el dispositivo existe antes de actualizar
    c = conn.cursor()
    c.execute('SELECT * FROM iot WHERE id = ?', (id,))
    row = c.fetchone()
    if not row:
        return {"error": -1}

    # Actualiza el valor del dispositivo en la base de datos
    c.execute('UPDATE iot SET value = ? WHERE id = ?', (value, id))
    conn.commit()

    # Retorna el resultado
    return {"value": value}

@app.delete("/iot/{id}")
async def eliminar_dispositivo(id: int):
    """Elimina un dispositivo."""
    c = conn.cursor()
    c.execute('DELETE FROM iot WHERE id = ?', (id,))
    conn.commit()
    return {"message": "Dispositivo eliminado"}