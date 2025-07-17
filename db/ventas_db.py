import sqlite3

def conectar():
    return sqlite3.connect("bazar.db")

# Crear o actualizar tabla de ventas con totales
def crear_tablas_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        total_neto REAL NOT NULL,
        total_iva REAL NOT NULL,
        total_final REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venta_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (venta_id) REFERENCES ventas(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    """)

    conn.commit()
    conn.close()

# Registrar una venta con totales (neto, iva, final)
def registrar_venta(carrito):
    import datetime
    conn = conectar()
    cursor = conn.cursor()

    total_final = sum(cantidad * precio for _, cantidad, precio, _ in carrito)
    total_neto = round(total_final / 1.19, 2)
    total_iva = round(total_final - total_neto, 2)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insertar en tabla ventas
    cursor.execute("INSERT INTO ventas (fecha, total_neto, total_iva, total_final) VALUES (?, ?, ?, ?)",
                   (fecha, total_neto, total_iva, total_final))
    venta_id = cursor.lastrowid

    # Insertar detalle de cada producto
    for nombre, cantidad, precio, producto_id in carrito:
        subtotal = cantidad * precio
        cursor.execute("""
            INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (venta_id, producto_id, cantidad, precio, subtotal))

    conn.commit()
    conn.close()
    return venta_id, total_neto, total_iva, total_final

# Obtener todas las ventas
def obtener_ventas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ventas ORDER BY fecha DESC")
    ventas = cursor.fetchall()
    conn.close()
    return ventas

# Obtener detalle de una venta específica
def obtener_detalle_venta(venta_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM detalle_ventas WHERE venta_id = ?", (venta_id,))
    detalles = cursor.fetchall()
    conn.close()
    return detalles