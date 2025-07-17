import customtkinter as ctk
from frames.login_frame import LoginFrame
from frames.admin_frame import AdminFrame
from frames.vendedor_frame import VendedorFrame
from frames.ventas_frame import VentasFrame
from frames.historial_ventas_frame import HistorialVentasFrame
from frames.detalle_venta_frame import DetalleVentaFrame
from frames.productos_frame import ProductosFrame
from frames.inventario_frame import InventarioFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bazar - Sistema de Gestión")
        self.overrideredirect(True)  # Sin bordes
        self.after(10, self.maximizar_manual)

        self.frames = {}
        for FrameClass in (LoginFrame, AdminFrame, VendedorFrame, VentasFrame, HistorialVentasFrame, DetalleVentaFrame, ProductosFrame, InventarioFrame):
            frame = FrameClass(self, self.cambiar_frame)
            self.frames[FrameClass.__name__] = frame

        self.cambiar_frame("LoginFrame")

    def maximizar_manual(self):
        ancho = self.winfo_screenwidth()
        alto = self.winfo_screenheight()
        self.geometry(f"{ancho}x{alto}+0+0")

    def cambiar_frame(self, nombre_frame, **kwargs):
        # Ocultar todos los frames actuales
        for frame in self.frames.values():
            frame.pack_forget()

        # Si es el frame de detalle de venta, lo creamos dinámicamente
        if nombre_frame == "DetalleVentaFrame":
            frame = DetalleVentaFrame(self, self.cambiar_frame, id_venta=kwargs.get("id_venta"))
            frame.pack(fill="both", expand=True)
            return

        # Mostrar los demás frames normalmente
        self.frames[nombre_frame].pack(fill="both", expand=True)

        # Actualizar datos según el frame
        if nombre_frame == "InventarioFrame":
            self.frames[nombre_frame].cargar_productos()
        elif nombre_frame == "ProductosFrame":
            self.frames[nombre_frame].cargar_productos()
        elif nombre_frame == "VentasFrame":
            self.frames[nombre_frame].cargar_productos()
        elif nombre_frame == "HistorialVentasFrame":
            self.frames[nombre_frame].cargar_ventas()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
