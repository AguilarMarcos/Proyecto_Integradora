import customtkinter as ctk 
from tkinter import messagebox, ttk
from products_controller import ver_productos, crear_producto, actualizar_producto, eliminar_producto
from database import crear_conexion


class ProductsApp:
    def __init__(self, root, dashboard_root):
        self.root = root
        self.dashboard_root = dashboard_root  
        self.root.title("Gestión de Productos")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        self.configurar_estilo_treeview(root)
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.crear_elementos()
        self.ver_productos()

    def configurar_estilo_treeview(self, root_widget): 
        style = ttk.Style()
        style.theme_use("default") 
        
        bg_color = root_widget._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = root_widget._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        
        style.configure("Treeview", 
                        background=bg_color,
                        foreground=text_color,
                        fieldbackground=bg_color,
                        bordercolor=bg_color,
                        borderwidth=0)
        style.map('Treeview', 
                  background=[('selected', '#3B82F6')])
        style.configure("Treeview.Heading", 
                        background=root_widget._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"]),
                        foreground=text_color,
                        font=('Arial', 12, 'bold'),
                        borderwidth=0)

    def crear_elementos(self):
        ctk.CTkLabel(
            self.main_frame, 
            text="Gestión de Productos",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=15)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="Ver Productos", command=self.ver_productos
        ).grid(row=0, column=0, padx=10, pady=5)

        ctk.CTkButton(
            btn_frame, text="Agregar Producto", command=self.crear_producto
        ).grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkButton(
            btn_frame, text="Actualizar Producto", command=self.actualizar_producto
        ).grid(row=0, column=2, padx=10, pady=5)

        ctk.CTkButton(
            btn_frame, text="Eliminar Producto", command=self.eliminar_producto, 
            fg_color="#F44336", hover_color="#D32F2F"
        ).grid(row=0, column=3, padx=10, pady=5)

        nav_btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav_btn_frame.pack(pady=15)
        
        ctk.CTkButton(
            nav_btn_frame, text="Volver al Dashboard", command=self.volver_dashboard, 
            width=200, height=40, fg_color="#424242", hover_color="#616161", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=20)

        ctk.CTkButton(
            nav_btn_frame, text="Salir del Sistema", command=self.salir_sistema, 
            width=200, height=40, fg_color="#D32F2F", hover_color="#C62828", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=1, padx=20)

        columns = ("ID", "Nombre", "Stock", "Precio", "Status", "Marca", "Proveedor", "Descripción")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, height=15, show='headings')
        
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor=ctk.CENTER)
        self.tree.heading("Nombre", text="Nombre del Producto")
        self.tree.column("Nombre", width=180, anchor=ctk.W)
        self.tree.heading("Stock", text="Stock")
        self.tree.column("Stock", width=80, anchor=ctk.CENTER)
        self.tree.heading("Precio", text="Precio")
        self.tree.column("Precio", width=100, anchor=ctk.E)
        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=80, anchor=ctk.CENTER)
        self.tree.heading("Marca", text="Marca")
        self.tree.column("Marca", width=100, anchor=ctk.W)
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.column("Proveedor", width=150, anchor=ctk.W)
        self.tree.heading("Descripción", text="Descripción")
        self.tree.column("Descripción", width=250, anchor=ctk.W)
        
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

    def ver_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        productos = ver_productos()
        for prod in productos:
            self.tree.insert("", "end", values=prod)

    def crear_producto(self):
        def guardar():
            nombre = entry_nombre.get().strip()
            stock_str = entry_stock.get().strip()
            precio_str = entry_precio.get().strip()
            status = status_var.get()
            marca = entry_marca.get().strip() or None
            proveedor = entry_proveedor.get().strip() or None
            descripcion = entry_descripcion.get().strip() or None

            if not nombre:
                messagebox.showwarning("Campo vacío", "El nombre es obligatorio.")
                return

            try:
                stock = int(stock_str) if stock_str else 0
                precio = float(precio_str) if precio_str else 0.0
            except ValueError:
                messagebox.showerror("Error", "Stock debe ser entero y Precio un número.")
                return

            if crear_producto(nombre, stock, precio, status, marca, proveedor, descripcion):
                messagebox.showinfo("Éxito", "Producto creado correctamente.")
                self.ver_productos()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el producto.")

        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Agregar Producto")
        ventana.geometry("500x750")
        ventana.transient(self.root)
        ventana.grab_set()

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

    
        ctk.CTkLabel(frame, text="Nombre:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 0))
        entry_nombre = ctk.CTkEntry(frame, width=350)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame, text="Stock:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_stock = ctk.CTkEntry(frame, width=350)
        entry_stock.pack(pady=5)

        ctk.CTkLabel(frame, text="Precio:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_precio = ctk.CTkEntry(frame, width=350)
        entry_precio.pack(pady=5)

        ctk.CTkLabel(frame, text="Status:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        status_var = ctk.StringVar(value="Activo")
        ctk.CTkOptionMenu(frame, values=["Activo", "Inactivo"], variable=status_var, width=350).pack(pady=5)

        ctk.CTkLabel(frame, text="Marca:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_marca = ctk.CTkEntry(frame, width=350)
        entry_marca.pack(pady=5)

        ctk.CTkLabel(frame, text="Proveedor:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_proveedor = ctk.CTkEntry(frame, width=350)
        entry_proveedor.pack(pady=5)

        ctk.CTkLabel(frame, text="Descripción:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_descripcion = ctk.CTkEntry(frame, width=350)
        entry_descripcion.pack(pady=5)

        ctk.CTkButton(frame, text="Guardar", command=guardar, width=200, font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=200, fg_color="gray").pack(pady=5)

    def actualizar_producto(self):
        def cargar_datos():
            product_id = entry_id.get().strip()
            if not product_id:
                messagebox.showwarning("Campo vacío", "Ingrese el ID del producto.")
                return False
            
            try:
                pid = int(product_id)
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")
                return False

            conexion = crear_conexion()
            if not conexion:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
                return False

            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT nombre_producto, stock, precio, status, marca, proveedor, descripcion 
                    FROM productos WHERE id_producto = %s
                """, (pid,))
                producto = cursor.fetchone()
                if not producto:
                    messagebox.showerror("No encontrado", f"No existe un producto con ID {pid}.")
                    return False

                entry_nombre.delete(0, ctk.END)
                entry_nombre.insert(0, producto[0] or "")

                entry_stock.delete(0, ctk.END)
                entry_stock.insert(0, str(producto[1]) if producto[1] is not None else "")

                entry_precio.delete(0, ctk.END)
                entry_precio.insert(0, str(producto[2]) if producto[2] is not None else "")

                status_var.set(producto[3] or "Activo")

                entry_marca.delete(0, ctk.END)
                entry_marca.insert(0, producto[4] or "")

                entry_proveedor.delete(0, ctk.END)
                entry_proveedor.insert(0, producto[5] or "")

                entry_descripcion.delete(0, ctk.END)
                entry_descripcion.insert(0, producto[6] or "")

                return True
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar datos: {e}")
                return False
            finally:
                if conexion and conexion.is_connected():
                    conexion.close()

        def guardar():
            product_id = entry_id.get().strip()
            if not product_id:
                messagebox.showwarning("Campo vacío", "Ingrese el ID del producto.")
                return

            try:
                pid = int(product_id)
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")
                return

            nombre = entry_nombre.get().strip()
            stock_str = entry_stock.get().strip()
            precio_str = entry_precio.get().strip()
            status = status_var.get()
            marca = entry_marca.get().strip() or None
            proveedor = entry_proveedor.get().strip() or None
            descripcion = entry_descripcion.get().strip() or None

            if not nombre:
                messagebox.showwarning("Campo requerido", "El nombre del producto es obligatorio.")
                return

            try:
                stock = int(stock_str) if stock_str else 0
                precio = float(precio_str) if precio_str else 0.0
            except ValueError:
                messagebox.showerror("Error", "Stock debe ser número entero y Precio un número.")
                return

            if actualizar_producto(pid, nombre, stock, precio, status, marca, proveedor, descripcion):
                messagebox.showinfo("Éxito", f"Producto con ID {pid} actualizado correctamente.")
                self.ver_productos()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar. Verifique el ID o los datos.")

        # === Ventana ===
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Actualizar Producto")
        ventana.geometry("500x750")
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.focus_force()

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # ID
        ctk.CTkLabel(frame, text="ID del Producto a actualizar:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 0))
        entry_id = ctk.CTkEntry(frame, width=350)
        entry_id.pack(pady=5)
        entry_id.bind("<Return>", lambda e: cargar_datos())

        ctk.CTkButton(frame, text="Cargar Datos", command=cargar_datos, width=200).pack(pady=(5, 10))

        # Campos
        ctk.CTkLabel(frame, text="Nombre:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_nombre = ctk.CTkEntry(frame, width=350)
        entry_nombre.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Stock:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_stock = ctk.CTkEntry(frame, width=350)
        entry_stock.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Precio:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_precio = ctk.CTkEntry(frame, width=350)
        entry_precio.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Status:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        status_var = ctk.StringVar(value="Activo")
        ctk.CTkOptionMenu(frame, values=["Activo", "Inactivo"], variable=status_var, width=350).pack(pady=5)
        
        ctk.CTkLabel(frame, text="Marca:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_marca = ctk.CTkEntry(frame, width=350)
        entry_marca.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Proveedor:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_proveedor = ctk.CTkEntry(frame, width=350)
        entry_proveedor.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Descripción:", font=ctk.CTkFont(weight="bold")).pack(pady=(5, 0))
        entry_descripcion = ctk.CTkEntry(frame, width=350)
        entry_descripcion.pack(pady=5)

        ctk.CTkButton(frame, text="Guardar Cambios", command=guardar, width=200, font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=200, fg_color="gray").pack(pady=5)

    def eliminar_producto(self):
        def eliminar():
            product_id = entry_id.get().strip()
            if not product_id:
                messagebox.showwarning("Campo vacío", "Ingrese el ID del producto a eliminar.")
                return
            
            try:
                product_id_int = int(product_id)
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")
                return

            conexion = crear_conexion()
            if not conexion:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
                return

            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre_producto FROM productos WHERE id_producto = %s", (product_id_int,))
                producto = cursor.fetchone()
                if not producto:
                    messagebox.showerror("No encontrado", f"No existe un producto con ID {product_id_int}.")
                    return

                confirm = messagebox.askyesno(
                    "Confirmar eliminación",
                    f"¿Eliminar el producto '{producto[0]}' (ID: {product_id_int})?"
                )
                if confirm:
                    if eliminar_producto(product_id_int):
                        messagebox.showinfo("Éxito", f"Producto '{producto[0]}' eliminado correctamente.")
                        self.ver_productos()
                        ventana.destroy()
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el producto.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar producto: {e}")
            finally:
                if conexion and conexion.is_connected():
                    conexion.close()

        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Eliminar Producto")
        ventana.geometry("400x220")
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.focus_force()

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="ID del producto a eliminar:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        entry_id = ctk.CTkEntry(frame, width=250)
        entry_id.pack(pady=5)
        entry_id.bind("<Return>", lambda e: eliminar())

        ctk.CTkButton(frame, text="Eliminar", command=eliminar, width=150, fg_color="#F44336", hover_color="#D32F2F", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=150, fg_color="gray").pack(pady=5)

    def volver_dashboard(self):
        self.root.destroy()
        if self.dashboard_root and self.dashboard_root.winfo_exists():
            self.dashboard_root.deiconify() 

    def salir_sistema(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir del sistema?"):
            self.root.destroy()
            if self.dashboard_root and self.dashboard_root.winfo_exists():
                 self.dashboard_root.destroy()
            self.root.quit()