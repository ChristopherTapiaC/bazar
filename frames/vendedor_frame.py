import customtkinter as ctk
from tkinter import messagebox

class VendedorFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame

        ctk.CTkLabel(self, text="Panel de Ventas", font=("Arial", 36)).pack(pady=40)

        ctk.CTkButton(self, text="💰 Registrar Venta",
                      font=("Arial", 20), width=400, height=60,
                      command=self.registrar_venta).pack(pady=30)

        ctk.CTkButton(self, text="Cerrar Sesión",
                      font=("Arial", 18), fg_color="red", width=300, height=50,
                      command=self.confirmar_cierre_sesion).pack(pady=30)

    def registrar_venta(self):
        messagebox.showinfo("Venta", "Aquí irá el módulo de registro de ventas.")

    def confirmar_cierre_sesion(self):
        confirm = messagebox.askyesno("Cerrar Sesión", "¿Deseas cerrar sesión?")
        if confirm:
            self.cambiar_frame("LoginFrame")
