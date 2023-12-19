# this example shows how to communicate with a database
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str
    price: float


conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Create table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS items (
        name text PRIMARY KEY,
        description text,
        price real
    )
    """
)
conn.commit()

app = FastAPI()


@app.post("/items")
async def create_item(item: Item):
    try:
        cursor.execute(
            "INSERT INTO items VALUES (?, ?, ?)",
            (item.name, item.description, item.price),
            # never do this:
            # f"INSERT INTO items VALUES ({item.name} {item.description} {item.price})",
            # item.name == "a'; DROP TABLE items; --"
        )
        conn.commit()
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items/{name}")
async def get_item(name: str) -> Item:
    try:
        cursor.execute("SELECT * FROM items WHERE name=?", (name,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return Item(name=row[0], description=row[1], price=row[2])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
