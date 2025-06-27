import customtkinter as ctk
from tkinter import messagebox

class AdminFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame

        ctk.CTkLabel(self, text="Panel del Administrador", font=("Arial", 36)).pack(pady=40)

        ctk.CTkButton(self, text="🛒 Gestión de Productos",
                      font=("Arial", 20), width=400, height=60,
                      command=self.gestion_productos).pack(pady=15)

        ctk.CTkButton(self, text="📦 Inventario / Bodega",
                      font=("Arial", 20), width=400, height=60,
                      command=self.inventario).pack(pady=15)

        ctk.CTkButton(self, text="📊 Reportes de Venta",
                      font=("Arial", 20), width=400, height=60,
                      command=self.reportes).pack(pady=15)

        ctk.CTkButton(self, text="Cerrar Sesión",
                      font=("Arial", 18), fg_color="red", width=300, height=50,
                      command=self.confirmar_cierre_sesion).pack(pady=30)

    def gestion_productos(self):
        self.cambiar_frame("ProductosFrame")

    def inventario(self):
        messagebox.showinfo("Inventario", "Aquí irá la gestión de inventario.")

    def reportes(self):
        messagebox.showinfo("Reportes", "Aquí irá la generación de reportes.")

    def confirmar_cierre_sesion(self):
        confirm = messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que deseas cerrar sesión?")
        if confirm:
            self.cambiar_frame("LoginFrame")