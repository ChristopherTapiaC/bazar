import customtkinter as ctk
from tkinter import messagebox
from db import productos_db

class InventarioFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame

        ctk.CTkLabel(self, text="Gestión de Inventario", font=("Arial", 36)).pack(pady=30)

        # Lista de productos con stock
        self.lista = ctk.CTkTextbox(self, width=600, height=300, font=("Consolas", 16))
        self.lista.pack(pady=10)
        self.lista._textbox.tag_configure("bajo_stock", foreground="red")
        productos_db.crear_tabla_productos()
        self.cargar_productos()

        # Formulario para modificar stock
        ctk.CTkLabel(self, text="Modificar Stock", font=("Arial", 20)).pack(pady=20)

        self.id_producto = ctk.CTkEntry(self, placeholder_text="ID del producto", font=("Arial", 16), width=200)
        self.id_producto.pack(pady=5)

        self.nuevo_stock = ctk.CTkEntry(self, placeholder_text="Nuevo stock", font=("Arial", 16), width=200)
        self.nuevo_stock.pack(pady=5)

        ctk.CTkButton(self, text="Actualizar Stock", font=("Arial", 16), width=300,
                      command=self.actualizar_stock).pack(pady=15)

        ctk.CTkButton(self, text="⬅️ Volver", font=("Arial", 16), width=200,
                      command=lambda: self.cambiar_frame("AdminFrame")).pack(pady=30)

    def cargar_productos(self):
        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")
        productos = productos_db.obtener_productos()
        self.lista.insert("end", f"{'ID':<5}{'Nombre':<25}{'Stock':<10}\n")
        self.lista.insert("end", "-"*60 + "\n")
        for p in productos:
            if p[3] == 0:
                linea = f"{p[0]:<5}{p[1]:<25}{p[3]:<10} ⚠ SIN STOCK ⚠\n"
            elif p[3] <= 5:
                linea = f"{p[0]:<5}{p[1]:<25}{p[3]:<10} ⚠ Bajo stock\n"
            else:
                linea = f"{p[0]:<5}{p[1]:<25}{p[3]:<10}\n"
            self.lista.insert("end", linea)
            if p[3] <= 5:
                linea_index = self.lista.index("end - 1 lines")
                self.lista._textbox.tag_add("bajo_stock", linea_index, f"{linea_index} lineend")
        self.lista.configure(state="disabled")

    def actualizar_stock(self):
        try:
            id_ = int(self.id_producto.get())
            stock = int(self.nuevo_stock.get())
            conn = productos_db.conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (stock, id_))
            conn.commit()
            conn.close()
            self.cargar_productos()
            messagebox.showinfo("Éxito", "Stock actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el stock: {e}")
