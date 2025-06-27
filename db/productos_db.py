import sqlite3

def conectar():
    return sqlite3.connect("bazar.db")

def crear_tabla_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def agregar_producto(nombre, precio, stock):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))
    conn.commit()
    conn.close()

def editar_producto(id_producto, nuevo_nombre, nuevo_precio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE id = ?", (nuevo_nombre, nuevo_precio, id_producto))
    conn.commit()
    conn.close()

def eliminar_producto(id_producto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()
