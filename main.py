import customtkinter as ctk
from frames.login_frame import LoginFrame
from frames.admin_frame import AdminFrame
from frames.vendedor_frame import VendedorFrame
from frames.productos_frame import ProductosFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bazar - Sistema de Gestión")
        self.overrideredirect(True)  # Sin bordes
        self.after(10, self.maximizar_manual)

        self.frames = {}
        for FrameClass in (LoginFrame, AdminFrame, VendedorFrame, ProductosFrame):
            frame = FrameClass(self, self.cambiar_frame)
            self.frames[FrameClass.__name__] = frame

        self.cambiar_frame("LoginFrame")

    def maximizar_manual(self):
        ancho = self.winfo_screenwidth()
        alto = self.winfo_screenheight()
        self.geometry(f"{ancho}x{alto}+0+0")

    def cambiar_frame(self, nombre_frame):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[nombre_frame].pack(fill="both", expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
