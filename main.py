# app.py

from fastapi import FastAPI, HTTPException
from typing import Optional
import sqlite3
import os

app = FastAPI()

# Database setup (in-memory SQLite for simplicity)
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)')
cursor.executemany('INSERT INTO items (name) VALUES (?)', [('Item A',), ('Item B',), ('Item C',)])
conn.commit()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    cursor.execute('SELECT name FROM items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    if item:
        return {"id": item_id, "name": item[0]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/users/{user_id}")
def read_user(user_id: int):
    # Mock user data
    return {"user_id": user_id, "username": f"user{user_id}"}

@app.get("/ping")
def ping(host: str):
    """
    Pings a host and returns the result.
    """
    command = f"ping -c 1 {host}"
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return {"output": result}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail="Ping failed") from e

@app.get("/files")
def read_file(filename: str):
    # Secure endpoint
    base_dir = os.path.join(os.path.dirname(__file__), "safe_directory")
    file_path = os.path.join(base_dir, filename)
    if os.path.commonprefix((os.path.realpath(file_path), base_dir)) != base_dir:
        raise HTTPException(status_code=400, detail="Invalid file path")
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
