

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="."), name="static")
DB_FILE = "database.json"

def read_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.get("/", response_class=HTMLResponse)
async def get_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200, headers={"Content-Type": "text/html; charset=utf-8"})

@app.get("/items")
async def get_items():
    return read_db()

@app.post("/items")
async def create_item(request: Request):
    data = await request.json()
    items = read_db()
    item_type = data.get("type")
    new_item = {"id": str(uuid.uuid4()), "type": item_type}
    # Notas
    if item_type == "nota":
        new_item["category"] = data.get("category", "")
        new_item["title"] = data.get("title", "")
        new_item["text"] = data.get("text", "")
    # Tareas
    elif item_type == "tarea":
        new_item["category"] = data.get("category", "")
        new_item["title"] = data.get("title", "")
        new_item["start"] = data.get("start", "")
        new_item["end"] = data.get("end", "")
        new_item["budget"] = data.get("budget", None)
    # Presupuestos
    elif item_type == "presupuesto":
        new_item["category"] = data.get("category", "")
        new_item["title"] = data.get("title", "")
        new_item["link"] = data.get("link", "")
        new_item["price"] = data.get("price", None)
    else:
        return JSONResponse(content={"error": "Tipo inválido"}, status_code=400)
    items.append(new_item)
    write_db(items)
    return new_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    items = read_db()
    item_found = False
    for i, item in enumerate(items):
        if item.get("id") == item_id:
            items.pop(i)
            item_found = True
            break
    if not item_found:
        return JSONResponse(content={"error": "Item not found"}, status_code=404)
    write_db(items)
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        log_level="info"
    )