import customtkinter as ctk
from login_view import LoginApp


def main():
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")  
    
    root = ctk.CTk()
    app = LoginApp(root)
    root.mainloop()  

if __name__ == "__main__":
    main()