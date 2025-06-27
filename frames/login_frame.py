import customtkinter as ctk
from tkinter import messagebox

usuarios = {
    "admin": {"clave": "admin123", "rol": "administrador"},
    "vendedor": {"clave": "venta123", "rol": "vendedor"}
}

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame

        ctk.CTkLabel(self, text="Sistema de Gestión - Bazar", font=("Arial", 36)).pack(pady=40)

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", font=("Arial", 20), width=400, height=50)
        self.entry_usuario.pack(pady=15)

        self.entry_clave = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", font=("Arial", 20), width=400, height=50)
        self.entry_clave.pack(pady=15)

        ctk.CTkButton(self, text="Ingresar", font=("Arial", 20), width=300, height=50, command=self.verificar_login).pack(pady=25)

        ctk.CTkButton(self, text="Entrar como Admin (demo)", font=("Arial", 16), fg_color="gray",
                      width=300, height=40, command=lambda: self.cambiar_frame("AdminFrame")).pack(pady=10)

        ctk.CTkButton(self, text="Entrar como Vendedor (demo)", font=("Arial", 16), fg_color="gray",
                      width=300, height=40, command=lambda: self.cambiar_frame("VendedorFrame")).pack(pady=10)

        ctk.CTkButton(self, text="Salir", font=("Arial", 16), fg_color="red",
                      width=300, height=40, command=self.salir).pack(pady=30)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()

        if usuario in usuarios and usuarios[usuario]["clave"] == clave:
            rol = usuarios[usuario]["rol"]
            if rol == "administrador":
                self.cambiar_frame("AdminFrame")
            else:
                self.cambiar_frame("VendedorFrame")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Deseas salir de la aplicación?"):
            self.master.destroy()