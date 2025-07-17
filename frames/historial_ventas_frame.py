import customtkinter as ctk
from tkinter import messagebox
from db import ventas_db

class HistorialVentasFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame

        ctk.CTkLabel(self, text="Historial de Ventas", font=("Arial", 28)).pack(pady=20)

        # Lista de ventas
        self.lista_ventas = ctk.CTkTextbox(self, width=700, height=300, font=("Consolas", 14))
        self.lista_ventas.pack(pady=10)
        self.cargar_ventas()

        # Campo para ver detalles
        ctk.CTkLabel(self, text="Ingrese ID de la venta para ver detalles", font=("Arial", 16)).pack(pady=5)
        self.id_venta = ctk.CTkEntry(self, placeholder_text="ID de Venta", font=("Arial", 14), width=200)
        self.id_venta.pack(pady=5)

        ctk.CTkButton(self, text="🔍 Ver Detalles", font=("Arial", 16), width=200, height=40,
                      command=self.ver_detalles).pack(pady=10)

        ctk.CTkButton(self, text="⬅️ Volver al Panel Admin", font=("Arial", 16), width=250, height=40,
                      command=lambda: self.cambiar_frame("AdminFrame")).pack(pady=20)

    def cargar_ventas(self):
        self.lista_ventas.configure(state="normal")
        self.lista_ventas.delete("1.0", "end")
        ventas = ventas_db.obtener_ventas()
        self.lista_ventas.insert("end", f"{'ID':<5}{'Fecha':<22}{'Neto':<12}{'IVA':<10}{'Total':<10}\n")
        self.lista_ventas.insert("end", "-" * 70 + "\n")
        for v in ventas:
            self.lista_ventas.insert("end", f"{v[0]:<5}{v[1]:<22}{v[2]:<12}{v[3]:<10}{v[4]:<10}\n")
        self.lista_ventas.configure(state="disabled")

    def ver_detalles(self):
        try:
            if not self.id_venta.get().strip():
                raise ValueError("Debe ingresar un ID de venta.")

            id_ = int(self.id_venta.get())
            ventas = [v[0] for v in ventas_db.obtener_ventas()]
            if id_ not in ventas:
                raise ValueError("No existe una venta con ese ID.")

            self.cambiar_frame("DetalleVentaFrame", id_venta=id_)
        except Exception as e:
            messagebox.showerror("Error", str(e))
