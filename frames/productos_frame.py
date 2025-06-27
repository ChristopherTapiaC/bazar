import customtkinter as ctk
from tkinter import messagebox
from db import productos_db

class ProductosFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame

        productos_db.crear_tabla_productos()

        # Título
        ctk.CTkLabel(self, text="Gestión de Productos", font=("Arial", 36)).pack(pady=30)

        # Lista de productos
        self.lista = ctk.CTkTextbox(self, width=600, height=300, font=("Consolas", 16))
        self.lista.pack(pady=10)
        self.lista.bind("<ButtonRelease-1>", self.seleccionar_producto)
        self.lista._textbox.tag_configure("resaltado", background="white", foreground="black")
        self.cargar_productos()

        # Entradas
        self.nombre = ctk.CTkEntry(self, placeholder_text="Nombre", font=("Arial", 18), width=420, height=30)
        self.nombre.pack(pady=5)

        # Crear contenedor horizontal
        fila = ctk.CTkFrame(self)
        fila.pack(pady=10)

        self.precio = ctk.CTkEntry(fila, placeholder_text="Precio", font=("Arial", 18), width=200, height=30)
        self.precio.pack(side="left", padx=10)

        self.stock = ctk.CTkEntry(fila, placeholder_text="Stock", font=("Arial", 18), width=200, height=30)
        self.stock.pack(side="left", padx=10)

        # Botón agregar
        ctk.CTkButton(self, text="➕ Agregar Producto", font=("Arial", 18), width=300, height=50,
                      command=self.agregar_producto).pack(pady=10)

        # Sección de edición
        ctk.CTkLabel(self, text="Modificar o Eliminar producto", font=("Arial", 20)).pack(pady=15)

        self.id_editar = ctk.CTkEntry(self, placeholder_text="ID del producto", font=("Arial", 16), width=200)
        self.id_editar.pack(pady=5)

        self.nombre_editar = ctk.CTkEntry(self, placeholder_text="Nuevo nombre", font=("Arial", 16), width=300)
        self.nombre_editar.pack(pady=5)

        self.precio_editar = ctk.CTkEntry(self, placeholder_text="Nuevo precio", font=("Arial", 16), width=300)
        self.precio_editar.pack(pady=5)

        # Contenedor horizontal para botones
        fila_botones = ctk.CTkFrame(self)
        fila_botones.pack(pady=10)

        ctk.CTkButton(fila_botones, text="✏️ Modificar", font=("Arial", 16), width=200,
                      command=self.modificar_producto).pack(side= "left", padx=10)

        ctk.CTkButton(fila_botones, text="🗑️ Eliminar", font=("Arial", 16), fg_color="red", width=200,
                      command=self.eliminar_producto).pack(side= "left", padx=10)

        # Volver
        ctk.CTkButton(self, text="⬅️ Volver al Panel", font=("Arial", 16), width=250, height=40,
                      command=lambda: self.cambiar_frame("AdminFrame")).pack(pady=10)

    def cargar_productos(self):
        self.lista.configure(state="normal")
        self.lista.delete("1.0", "end")
        productos = productos_db.obtener_productos()
        self.lista.insert("end", f"{'ID':<5}{'Nombre':<25}{'Precio':<10}{'Stock':<10}\n")
        self.lista.insert("end", "-"*60 + "\n")
        for p in productos:
            self.lista.insert("end", f"{p[0]:<5}{p[1]:<25}{p[2]:<10}{p[3]:<10}\n")
        self.lista.configure(state="disabled")

    def agregar_producto(self):
        try:
            nombre = self.nombre.get()
            precio = float(self.precio.get())
            stock = int(self.stock.get())
            if nombre == "":
                raise ValueError("El nombre no puede estar vacío")
            productos_db.agregar_producto(nombre, precio, stock)
            self.cargar_productos()
            self.nombre.delete(0, "end")
            self.precio.delete(0, "end")
            self.stock.delete(0, "end")
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def seleccionar_producto(self, event):
        try:
            self.lista.configure(state="normal")
            self.lista._textbox.tag_remove("resaltado", "1.0", "end")

            index = self.lista.index("@%d,%d linestart" % (event.x, event.y))
            linea = self.lista.get(index, f"{index} lineend").strip()

            if linea.startswith("ID") or linea.startswith("-") or linea == "":
                self.lista.configure(state="disabled")
                return

            self.lista._textbox.tag_add("resaltado", index, f"{index} lineend")

            partes = linea.split()
            id_ = partes[0]
            nombre = " ".join(partes[1:-2])
            precio = partes[-2]

            self.id_editar.delete(0, "end")
            self.nombre_editar.delete(0, "end")
            self.precio_editar.delete(0, "end")

            self.id_editar.insert(0, id_)
            self.nombre_editar.insert(0, nombre)
            self.precio_editar.insert(0, precio)
            self.lista.configure(state="disabled")

        except Exception as e:
            print("Error al seleccionar producto:", e)
            self.lista.configure(state="disabled")

    def modificar_producto(self):
        try:
            id_ = int(self.id_editar.get())
            nombre = self.nombre_editar.get()
            precio = float(self.precio_editar.get())
            if nombre == "":
                raise ValueError("El nombre no puede estar vacío")
            productos_db.editar_producto(id_, nombre, precio)
            self.cargar_productos()
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar: {e}")

    def eliminar_producto(self):
        try:
            id_ = int(self.id_editar.get())
            confirm = messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar el producto?")
            if confirm:
                productos_db.eliminar_producto(id_)
                self.cargar_productos()
                messagebox.showinfo("Éxito", "Producto eliminado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
