from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from swagger_ui import setup_swagger_ui

app = FastAPI(
    title="API Data Mahasiswa",
    description=(
        "CRUD data mahasiswa (nama, alamat, ipk, semester, hobi) "
        "dengan database in-memory. Status error: 404, 409, 422."
    ),
    version="2.0.0",
    docs_url=None,
)

setup_swagger_ui(app)


class Item(BaseModel):
    nama: Optional[str] = None
    alamat: Optional[str] = None
    ipk: Optional[float] = None
    semester: Optional[int] = None
    hobi: Optional[str] = None


items_db = {}

# Route root "/" sengaja tidak didaftarkan agar hanya ada 4 endpoint CRUD
# ditambah /docs dan /openapi.json, sesuai batasan project.


@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    if item_id in items_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    items_db[item_id] = item.model_dump()
    return {"message": "Item created successfully", "item": items_db[item_id]}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": items_db[item_id]}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.model_dump()
    return {"message": "Item updated successfully", "item": items_db[item_id]}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return {"message": "Item deleted successfully", "deleted_item": deleted_item}
