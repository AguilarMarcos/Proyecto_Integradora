import customtkinter as ctk
from tkinter import messagebox
from user_view import DashboardApp
from auth_controller import validar_credenciales

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure((0, 5), weight=1)
        
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        main_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            main_frame, 
            text="Bienvenido al sistema", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        ctk.CTkLabel(main_frame, text="Ingresa tu nombre de usuario:").pack(pady=(10, 0))
        self.username_entry = ctk.CTkEntry(main_frame, width=220)
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(main_frame, text="Ingresa tu contraseña:").pack(pady=(10, 0))
        self.password_entry = ctk.CTkEntry(main_frame, show="*", width=220)  
        self.password_entry.pack(pady=5)

        ctk.CTkButton(
            main_frame, 
            text="Iniciar Sesión", 
            command=self.login,
            font=ctk.CTkFont(weight="bold"),
            width=220
        ).pack(pady=(20, 10))

   
    def login(self):
        usuario = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Faltan datos", "Favor de ingresar el usuario y la contraseña")
            return  
        
        if validar_credenciales(usuario, password):
            messagebox.showinfo("Acceso permitido", f"Bienvenido, {usuario}")
            self.root.withdraw() 
            root_dashboard = ctk.CTkToplevel(self.root)
            DashboardApp(usuario, root_dashboard)
            root_dashboard.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")