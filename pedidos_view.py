import customtkinter as ctk 
from pedidos_controller import ver_pedido, actualizar_pedido
from tkinter import messagebox, ttk
import tkinter as tk

from pedidos_controller import ver_pedido, crear_pedido, actualizar_pedido, eliminar_pedido


class PedidosApp:
    def __init__(self, root, dashboard_root):
        self.root = root
        self.dashboard_root = dashboard_root  
        self.root.title("Gestión de Pedidos")
        self.root.geometry("1300x700")
        self.root.resizable(False, False)

        self.configurar_estilo_treeview(root)
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.crear_elementos()
        self.ver_pedidos()

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
        style.map('Treeview', background=[('selected', '#3B82F6')])
        style.configure("Treeview.Heading", 
                        background=root_widget._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"]),
                        foreground=text_color,
                        font=('Arial', 12, 'bold'),
                        borderwidth=0)

    def crear_elementos(self):

        ctk.CTkLabel(
            self.main_frame, 
            text="📦 Gestión de Pedidos",
            fg_color="#424242",  
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=15)

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Ver Pedidos 🔄", command=self.ver_pedidos).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Agregar Pedido ➕", command=self.crear_pedido).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Actualizar Pedido ✏️", command=self.actualizar_pedido).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Eliminar Pedido 🗑️", command=self.eliminar_pedido,
                    fg_color="#F44336", hover_color="#D32F2F").grid(row=0, column=3, padx=10, pady=5)

        nav_btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        nav_btn_frame.pack(pady=15)
        
        ctk.CTkButton(nav_btn_frame, text="Volver al Dashboard 🏠", command=self.volver_dashboard,
                      width=200, height=40, fg_color="#424242", hover_color="#616161",
                      font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=20)

        ctk.CTkButton(nav_btn_frame, text="Salir del Sistema 🚪", command=self.salir_sistema,
                      width=200, height=40, fg_color="#D32F2F", hover_color="#C62828",
                      font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=1, padx=20)

        # Configuración de tabla — AHORA CON LAS NUEVAS COLUMNAS
        columns = ("ID", "Cliente", "Fecha", "Descripción", "Precio Total", "Abono", "ID Empleado", "Total")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, height=15, show='headings')
        
        self.tree.heading("ID", text="ID Pedido")
        self.tree.column("ID", width=80, anchor=tk.CENTER)

        self.tree.heading("Cliente", text="Nombre del Cliente")
        self.tree.column("Cliente", width=200, anchor=tk.W)

        self.tree.heading("Fecha", text="Fecha de Entrega")
        self.tree.column("Fecha", width=150, anchor=tk.CENTER)

        self.tree.heading("Descripción", text="Descripción")
        self.tree.column("Descripción", width=300, anchor=tk.W)

        self.tree.heading("Precio Total", text="Precio Total")
        self.tree.column("Precio Total", width=100, anchor=tk.E)

        self.tree.heading("Abono", text="Abono")
        self.tree.column("Abono", width=100, anchor=tk.E)

        self.tree.heading("ID Empleado", text="ID Empleado")
        self.tree.column("ID Empleado", width=120, anchor=tk.CENTER)

        self.tree.heading("Total", text="Total")
        self.tree.column("Total", width=120, anchor=tk.E)

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def ver_pedidos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        pedidos = ver_pedido()



        for p in pedidos:
            id_pedido, cliente, fecha, descripcion, precio_total, abono, id_empleado = p

            total = precio_total - abono  

            self.tree.insert("", tk.END, values=(
                id_pedido, cliente, fecha, descripcion, precio_total, abono, id_empleado, total
            ))

    def crear_pedido(self):
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Agregar Pedido")
        ventana.geometry("500x650")
        ventana.transient(self.root)
        ventana.grab_set()

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # --- CAMPOS ---
        ctk.CTkLabel(frame, text="Nombre del Cliente:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        entry_nombre = ctk.CTkEntry(frame, width=350)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame, text="Fecha de Entrega (YYYY-MM-DD):", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        entry_fecha = ctk.CTkEntry(frame, width=350)
        entry_fecha.pack(pady=5)

        ctk.CTkLabel(frame, text="Descripción:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        entry_descripcion = ctk.CTkEntry(frame, width=350)
        entry_descripcion.pack(pady=5)

        ctk.CTkLabel(frame, text="Precio Total:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        entry_precio = ctk.CTkEntry(frame, width=350)
        entry_precio.pack(pady=5)

        ctk.CTkLabel(frame, text="Abono:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        entry_abono = ctk.CTkEntry(frame, width=350)
        entry_abono.pack(pady=5)

        ctk.CTkLabel(frame, text="ID Empleado:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        entry_empleado = ctk.CTkEntry(frame, width=350)
        entry_empleado.pack(pady=5)

    # --- GUARDAR ---
        def guardar():
            nombre = entry_nombre.get().strip()
            fecha = entry_fecha.get().strip()
            descripcion = entry_descripcion.get().strip()
            id_empleado = entry_empleado.get().strip()

            try:
                precio = float(entry_precio.get().strip())
                abono = float(entry_abono.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Precio y abono deben ser números.")
                return

            if not nombre or not fecha or not descripcion or not id_empleado:
                messagebox.showwarning("Campos obligatorios", "Debe llenar todos los campos.")
                return

            if crear_pedido(nombre, fecha, descripcion, precio, abono, id_empleado):
                messagebox.showinfo("Éxito", "Pedido creado correctamente.")
                self.ver_pedidos()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el pedido.")

        ctk.CTkButton(frame, text="Guardar Pedido", command=guardar, width=200).pack(pady=15)
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=200, fg_color="gray").pack()

    def actualizar_pedido(self):
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Actualizar Pedido")
        ventana.geometry("500x700")
        ventana.transient(self.root)
        ventana.grab_set()

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # ===== CAMPOS =====
        ctk.CTkLabel(frame, text="ID del Pedido:", font=ctk.CTkFont(weight="bold")).pack()
        entry_id = ctk.CTkEntry(frame, width=350)
        entry_id.pack(pady=5)

        # Botón cargar dentro de la ventana y con estilo CTK
        def cargar():
            from pedidos_controller import obtener_pedido_por_id
            pid = entry_id.get()

            if not pid.isdigit():
                messagebox.showwarning("Error", "Ingresa un ID válido")
                return

            pedido = obtener_pedido_por_id(pid)

            if not pedido:
                messagebox.showerror("Error", "No se encontró el pedido")
                return

            # Llenamos todos los campos
            entry_nombre.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)
            entry_descripcion.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
            entry_abono.delete(0, tk.END)
            entry_empleado.delete(0, tk.END)

            entry_nombre.insert(0, pedido["nombre_cliente"])
            entry_fecha.insert(0, str(pedido["fecha_entrega"]))
            entry_descripcion.insert(0, pedido["descripcion"])
            entry_precio.insert(0, str(pedido["precio_total"]))
            entry_abono.insert(0, str(pedido["abono"]))
            entry_empleado.insert(0, str(pedido["id_empleado"]))

        ctk.CTkButton(frame, text="Cargar Datos 🔍", command=cargar, width=200).pack(pady=10)

        # Resto de campos del formulario
        ctk.CTkLabel(frame, text="Nombre del Cliente:", font=ctk.CTkFont(weight="bold")).pack()
        entry_nombre = ctk.CTkEntry(frame, width=350)
        entry_nombre.pack(pady=5)

        ctk.CTkLabel(frame, text="Fecha de Entrega:", font=ctk.CTkFont(weight="bold")).pack()
        entry_fecha = ctk.CTkEntry(frame, width=350)
        entry_fecha.pack(pady=5)

        ctk.CTkLabel(frame, text="Descripción:", font=ctk.CTkFont(weight="bold")).pack()
        entry_descripcion = ctk.CTkEntry(frame, width=350)
        entry_descripcion.pack(pady=5)

        ctk.CTkLabel(frame, text="Precio Total:", font=ctk.CTkFont(weight="bold")).pack()
        entry_precio = ctk.CTkEntry(frame, width=350)
        entry_precio.pack(pady=5)

        ctk.CTkLabel(frame, text="Abono:", font=ctk.CTkFont(weight="bold")).pack()
        entry_abono = ctk.CTkEntry(frame, width=350)
        entry_abono.pack(pady=5)

        ctk.CTkLabel(frame, text="ID Empleado:", font=ctk.CTkFont(weight="bold")).pack()
        entry_empleado = ctk.CTkEntry(frame, width=350)
        entry_empleado.pack(pady=5)

        # ===== GUARDAR =====
        def guardar():
            try:
                pid = int(entry_id.get())
                nombre = entry_nombre.get().strip()
                fecha = entry_fecha.get().strip()
                descripcion = entry_descripcion.get().strip()
                precio = float(entry_precio.get().strip())
                abono = float(entry_abono.get().strip())
                empleado = int(entry_empleado.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos")
                return

            if actualizar_pedido(pid, nombre, fecha, descripcion, precio, abono, empleado):
                messagebox.showinfo("Éxito", "Pedido actualizado correctamente")
                self.ver_pedidos()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el pedido")

        ctk.CTkButton(frame, text="Guardar Cambios", command=guardar, width=200).pack(pady=15)
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=200, fg_color="gray").pack()

    
    
    
    
    
    
    
    
    
    
    def eliminar_pedido(self):
        def eliminar():
            pedido_id = entry_id.get().strip()
            if not pedido_id:
                messagebox.showwarning("Campo vacío", "Ingrese el ID del pedido a eliminar.")
                return
            
            try:
                pedido_id = int(pedido_id)
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número.")
                return

            if messagebox.askyesno("Confirmar", f"¿Desea eliminar el pedido {pedido_id}?"):
                if eliminar_pedido(pedido_id):
                    messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
                    self.ver_pedidos()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el pedido.")

        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Eliminar Pedido")
        ventana.geometry("350x200")
        ventana.transient(self.root)
        ventana.grab_set()

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="ID del Pedido:", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        entry_id = ctk.CTkEntry(frame, width=200)
        entry_id.pack(pady=5)
        ctk.CTkButton(frame, text="Eliminar", command=eliminar, width=150, fg_color="#F44336").pack(pady=10)
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=150, fg_color="gray").pack(pady=5)

    def volver_dashboard(self):
        self.root.destroy()
        if self.dashboard_root and self.dashboard_root.winfo_exists():
            self.dashboard_root.deiconify()

    def salir_sistema(self):
        if messagebox.askyesno("Salir", "¿Seguro que deseas salir del sistema?"):
            self.root.destroy()
            if self.dashboard_root and self.dashboard_root.winfo_exists():
                self.dashboard_root.destroy()
            self.root.quit()
