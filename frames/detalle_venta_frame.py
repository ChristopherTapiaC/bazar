import customtkinter as ctk
from tkinter import messagebox
from db import ventas_db

class DetalleVentaFrame(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame, id_venta=None):
        super().__init__(master)
        self.cambiar_frame = cambiar_frame
        self.id_venta = id_venta

        ctk.CTkLabel(self, text=f"Detalle de la Venta #{self.id_venta}", font=("Arial", 28)).pack(pady=20)

        # Lista de productos en la venta
        self.lista_detalle = ctk.CTkTextbox(self, width=700, height=300, font=("Consolas", 14))
        self.lista_detalle.pack(pady=10)
        self.cargar_detalle()

        ctk.CTkButton(self, text="⬅️ Volver al Historial", font=("Arial", 16), width=250, height=40,
                      command=self.volver_al_historial).pack(pady=20)

    def volver_al_historial(self):
        """Destruye el frame actual antes de volver al historial."""
        self.destroy()  # ✅ Elimina este frame
        self.cambiar_frame("HistorialVentasFrame")  # ✅ Regresa al historial

    def cargar_detalle(self):
        try:
            detalles = ventas_db.obtener_detalle_venta(self.id_venta)
            venta_info = [v for v in ventas_db.obtener_ventas() if v[0] == self.id_venta]

            self.lista_detalle.configure(state="normal")
            self.lista_detalle.delete("1.0", "end")
            self.lista_detalle.insert("end", f"{'Producto_ID':<12}{'Cant.':<10}{'Precio':<10}{'Subtotal':<10}\n")
            self.lista_detalle.insert("end", "-" * 60 + "\n")

            for d in detalles:
                self.lista_detalle.insert("end", f"{d[2]:<12}{d[3]:<10}{d[4]:<10}{d[5]:<10}\n")

            self.lista_detalle.insert("end", "-" * 60 + "\n")
            if venta_info:
                _, fecha, neto, iva, total = venta_info[0]
                self.lista_detalle.insert("end", f"Fecha: {fecha}\n")
                self.lista_detalle.insert("end", f"Total Neto: ${neto}\n")
                self.lista_detalle.insert("end", f"IVA (19%): ${iva}\n")
                self.lista_detalle.insert("end", f"Total Final: ${total}\n")

            self.lista_detalle.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el detalle: {e}")
