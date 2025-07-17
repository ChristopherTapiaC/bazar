import customtkinter as ctk
from tkinter import messagebox
from db import productos_db
from db import ventas_db

class VentasFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame
        self.carrito = []  # (nombre, cantidad, precio, producto_id)

        ventas_db.crear_tablas_ventas()

        ctk.CTkLabel(self, text="Registro de Ventas - Carrito de Compras", font=("Arial", 28)).pack(pady=20)

        # Lista de productos disponibles
        self.lista = ctk.CTkTextbox(self, width=600, height=200, font=("Consolas", 16))
        self.lista.pack(pady=10)
        self.cargar_productos()

        # Campos para agregar productos al carrito
        ctk.CTkLabel(self, text="Agregar al Carrito", font=("Arial", 20)).pack(pady=10)

        self.id_producto = ctk.CTkEntry(self, placeholder_text="ID del producto", font=("Arial", 16), width=200)
        self.id_producto.pack(pady=5)

        self.cantidad = ctk.CTkEntry(self, placeholder_text="Cantidad", font=("Arial", 16), width=200)
        self.cantidad.pack(pady=5)

        ctk.CTkButton(self, text="➕ Agregar al Carrito", font=("Arial", 16), width=250, height=40,
                      command=self.agregar_al_carrito).pack(pady=10)

        # Carrito de compras
        ctk.CTkLabel(self, text="Carrito Actual", font=("Arial", 20)).pack(pady=10)
        self.lista_carrito = ctk.CTkTextbox(self, width=600, height=150, font=("Consolas", 16))
        self.lista_carrito.pack(pady=5)

        # Botones finales
        ctk.CTkButton(self, text="✅ Generar Boleta", font=("Arial", 18), width=300, height=40,
                      command=self.finalizar_venta).pack(pady=10)

        ctk.CTkButton(self, text="⬅️ Volver al Panel", font=("Arial", 16), width=250, height=40,
                      command=lambda: self.cambiar_frame("VendedorFrame")).pack(pady=20)

        self.actualizar_carrito()

    def cargar_productos(self):
        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")
        productos = productos_db.obtener_productos()
        self.lista.insert("end", f"{'ID':<5}{'Nombre':<25}{'Precio':<10}{'Stock':<10}\n")
        self.lista.insert("end", "-"*60 + "\n")
        for p in productos:
            self.lista.insert("end", f"{p[0]:<5}{p[1]:<25}{p[2]:<10}{p[3]:<10}\n")
        self.lista.configure(state="disabled")

    def actualizar_carrito(self):
        self.lista_carrito.configure(state="normal")
        self.lista_carrito.delete("1.0", "end")
        total_final = sum(cantidad * precio for _, cantidad, precio, _ in self.carrito)
        total_neto = round(total_final / 1.19, 2) if total_final else 0
        total_iva = round(total_final - total_neto, 2) if total_final else 0

        self.lista_carrito.insert("end", f"{'Producto':<25}{'Cant.':<8}{'Precio':<10}{'Subtotal':<10}\n")
        self.lista_carrito.insert("end", "-"*60 + "\n")
        for item in self.carrito:
            nombre, cantidad, precio_unit, _ = item
            subtotal = cantidad * precio_unit
            self.lista_carrito.insert("end", f"{nombre:<25}{cantidad:<8}{precio_unit:<10}{subtotal:<10}\n")
        self.lista_carrito.insert("end", "-"*60 + "\n")
        self.lista_carrito.insert("end", f"NETO:{total_neto:>46}\n")
        self.lista_carrito.insert("end", f"IVA (19%):{total_iva:>40}\n")
        self.lista_carrito.insert("end", f"TOTAL:{total_final:>44}\n")
        self.lista_carrito.configure(state="disabled")

    def agregar_al_carrito(self):
        try:
            if not self.id_producto.get().strip() or not self.cantidad.get().strip():
                raise ValueError("Debe ingresar ID y cantidad.")

            id_ = int(self.id_producto.get())
            cantidad = int(self.cantidad.get())

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            conn = productos_db.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, precio, stock FROM productos WHERE id = ?", (id_,))
            producto = cursor.fetchone()
            conn.close()

            if not producto:
                raise ValueError("El producto no existe.")

            nombre, precio, stock_actual = producto
            if stock_actual < cantidad:
                raise ValueError("Stock insuficiente.")

            self.carrito.append((nombre, cantidad, precio, id_))

            self.id_producto.delete(0, "end")
            self.cantidad.delete(0, "end")
            self.actualizar_carrito()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar al carrito: {e}")

    def finalizar_venta(self):
        if not self.carrito:
            messagebox.showerror("Error", "El carrito está vacío.")
            return
        try:
            total_final = sum(cantidad * precio for _, cantidad, precio, _ in self.carrito)
            total_neto = round(total_final / 1.19, 2)
            total_iva = round(total_final - total_neto, 2)

            # Registrar la venta en la base de datos
            venta_id, _, _, _ = ventas_db.registrar_venta(self.carrito)

            # Actualizar stock en la base de datos
            conn = productos_db.conectar()
            cursor = conn.cursor()
            for item in self.carrito:
                _, cantidad, _, producto_id = item
                cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
                stock_actual = cursor.fetchone()[0]
                nuevo_stock = stock_actual - cantidad
                cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, producto_id))
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Venta completada",
                f"Venta #{venta_id} realizada correctamente.\n"
                f"Total Neto: ${total_neto}\n"
                f"IVA (19%): ${total_iva}\n"
                f"Total Final: ${total_final}"
            )

            self.carrito.clear()
            self.actualizar_carrito()
            self.cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo finalizar la venta: {e}")
