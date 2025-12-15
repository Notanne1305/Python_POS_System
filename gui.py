"""
GUI module - User interface for POS System
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
from products import ProductManager
from functions import POSFunctions

class POSWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("POS System - Point of Sale")
        self.root.geometry("550x600")  # Back to original height
        self.root.resizable(False, False)
        
        # Initialize managers
        self.product_manager = ProductManager()
        self.pos_functions = POSFunctions(self.product_manager)
        
        self.setup_main_window()
    
    def setup_main_window(self):
        # Top section - Input fields
        top_frame = tk.Frame(self.root, bg="white")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Configure grid columns to fill entire width
        top_frame.columnconfigure(1, weight=1)  # Product dropdown column
        top_frame.columnconfigure(3, weight=1)  # Price entry column
        top_frame.columnconfigure(5, weight=1)  # Qty entry column
        
        # Product dropdown
        tk.Label(top_frame, text="Product:", bg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(top_frame, textvariable=self.product_var, 
                                         values=self.product_manager.get_product_names(), 
                                         state="readonly")
        self.product_combo.grid(row=0, column=1, padx=5, sticky="ew")
        self.product_combo.bind("<<ComboboxSelected>>", self.on_product_select)
        
        # Price entry
        tk.Label(top_frame, text="Price:", bg="white").grid(row=0, column=2, sticky="w", padx=5)
        self.price_var = tk.StringVar()
        self.price_entry = tk.Entry(top_frame, textvariable=self.price_var, state="readonly")
        self.price_entry.grid(row=0, column=3, padx=5, sticky="ew")
        
        # Quantity entry
        tk.Label(top_frame, text="Qty:", bg="white").grid(row=0, column=4, sticky="w", padx=5)
        self.qty_var = tk.StringVar(value="1")
        self.qty_entry = tk.Entry(top_frame, textvariable=self.qty_var, relief="solid", borderwidth=1)
        self.qty_entry.grid(row=0, column=5, padx=5, sticky="ew")
        
        # Button frame (Original buttons)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Configure grid to make buttons fill space equally
        for i in range(5):
            btn_frame.columnconfigure(i, weight=1, uniform="button")
        
        # Buttons with grid layout to fill space
        tk.Button(btn_frame, text="Add", bg="#5cb85c", fg="white", command=self.add_item).grid(row=0, column=0, sticky="ew", padx=1)
        tk.Button(btn_frame, text="Update", bg="#5bc0de", fg="white", command=self.update_item).grid(row=0, column=1, sticky="ew", padx=1)
        tk.Button(btn_frame, text="Delete", bg="#d9534f", fg="white", command=self.delete_item).grid(row=0, column=2, sticky="ew", padx=1)
        tk.Button(btn_frame, text="Clear", bg="#999999", fg="white", command=self.clear_cart).grid(row=0, column=3, sticky="ew", padx=1)
        tk.Button(btn_frame, text="Purchase", bg="#17a2b8", fg="white", command=self.complete_purchase).grid(row=0, column=4, sticky="ew", padx=1)
        
        # Cart table
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for cart
        columns = ("Product", "Price", "Quantity", "Total")
        self.cart_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=130, anchor="center")
        
        # Configure style for gray background
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", 
                       background="#d3d3d3",  # Light gray background
                       foreground="black", 
                       fieldbackground="#d3d3d3")  # Gray for empty space
        style.map('Treeview', background=[('selected', '#a9a9a9')])  # Darker gray when selected
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bottom section - Totals, Manage Products, and Exit button
        bottom_frame = tk.Frame(self.root, bg="white")
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Left side: Manage Products button
        tk.Button(bottom_frame, text="Manage Products", bg="#8b4789", fg="white", 
                 command=self.open_product_management).pack(side=tk.LEFT)
        
        # Right side: Total labels and Exit button
        right_frame = tk.Frame(bottom_frame, bg="white")
        right_frame.pack(side=tk.RIGHT)
        
        # Exit button on the right
        tk.Button(right_frame, text="Exit", bg="#d9534f", fg="white", 
                 command=self.exit_application, width=10).pack(side=tk.RIGHT, padx=5)
        
        # Total labels
        self.total_label = tk.Label(right_frame, text="Total: ₱0.00", 
                                   font=("Arial", 12, "bold"), fg="#5cb85c", bg="white")
        self.total_label.pack(side=tk.RIGHT, padx=10)
        
        self.grand_total_label = tk.Label(right_frame, text="Grand Total (incl. tax): ₱0.00", 
                                         font=("Arial", 10), fg="#17a2b8", bg="white")
        self.grand_total_label.pack(side=tk.RIGHT, padx=10)
    
    def on_product_select(self, event):
        product_name = self.product_var.get()
        product = self.product_manager.get_product(product_name)
        if product:
            self.price_var.set(f"{product['price']:.2f}")
    
    def add_item(self):
        product_name = self.product_var.get()
        try:
            quantity = int(self.qty_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
            return
        
        if not product_name:
            messagebox.showerror("Error", "Please select a product")
            return
        
        product = self.product_manager.get_product(product_name)
        if product and product["stock"] >= quantity:
            self.pos_functions.add_to_cart(product_name, quantity)
            self.update_cart_display()
            self.qty_var.set("1")
        else:
            messagebox.showerror("Error", "Insufficient stock")
    
    def update_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to update")
            return
        
        try:
            quantity = int(self.qty_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
            return
        
        index = self.cart_tree.index(selected[0])
        self.pos_functions.update_cart_item(index, quantity)
        self.update_cart_display()
    
    def delete_item(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to delete")
            return
        
        index = self.cart_tree.index(selected[0])
        self.pos_functions.delete_cart_item(index)
        self.update_cart_display()
    
    def clear_cart(self):
        self.pos_functions.clear_cart()
        self.update_cart_display()
    
    def complete_purchase(self):
        if not self.pos_functions.get_cart_items():
            messagebox.showwarning("Warning", "Cart is empty")
            return
        
        grand_total = self.pos_functions.calculate_grand_total()
        if messagebox.askyesno("Confirm Purchase", f"Total amount: ₱{grand_total:.2f}\nComplete purchase?"):
            # Generate receipt
            receipt_content = self.generate_receipt()
            
            # Show receipt window (which now includes print button)
            self.show_receipt(receipt_content)
            
            # Save receipt automatically after purchase
            self.save_receipt_to_file(receipt_content, auto_save=True)
            
            # Complete purchase
            self.pos_functions.complete_purchase()
            self.update_cart_display()
            self.product_combo['values'] = self.product_manager.get_product_names()
    
    def exit_application(self):
        """Exit the application with confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    
    def generate_receipt(self):
        """Generate receipt content string"""
        receipt = "=" * 45 + "\n"
        receipt += " POS SYSTEM RECEIPT\n"
        receipt += "=" * 45 + "\n"
        receipt += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += "=" * 45 + "\n\n"
        receipt += f"{'Item':<20} {'Qty':<5} {'Price':<10} {'Total':<10}\n"
        receipt += "-" * 45 + "\n"
        
        for item in self.pos_functions.get_cart_items():
            receipt += f"{item['product']:<20} {item['quantity']:<5} "
            receipt += f"₱{item['price']:<9.2f} ₱{item['total']:<9.2f}\n"
        
        receipt += "-" * 45 + "\n"
        subtotal = self.pos_functions.calculate_subtotal()
        tax = self.pos_functions.calculate_tax()
        grand_total = self.pos_functions.calculate_grand_total()
        
        receipt += f"\n{'Subtotal:':<35} ₱{subtotal:>8.2f}\n"
        receipt += f"{'Tax (12%):':<35} ₱{tax:>8.2f}\n"
        receipt += "=" * 45 + "\n"
        receipt += f"{'GRAND TOTAL:':<35} ₱{grand_total:>8.2f}\n"
        receipt += "=" * 45 + "\n\n"
        receipt += " Thank you for your purchase!\n"
        receipt += " Please come again!\n"
        receipt += "=" * 45 + "\n"
        
        return receipt
    
    def show_receipt(self, receipt_content):
        """Display receipt in a new window with Print and Close buttons"""
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")
        receipt_window.geometry("450x550")  # Slightly larger to accommodate buttons
        receipt_window.resizable(False, False)
        
        # Main content frame
        main_frame = tk.Frame(receipt_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Receipt text widget with scrollbar
        text_frame = tk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        receipt_text = tk.Text(text_frame, width=50, height=25, font=("Courier", 10),
                              yscrollcommand=scrollbar.set)
        receipt_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=receipt_text.yview)
        
        receipt_text.insert("1.0", receipt_content)
        receipt_text.config(state="disabled")
        
        # Button frame at the bottom of the receipt window
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Print and Close buttons
        tk.Button(btn_frame, text="Print Receipt", bg="#5cb85c", fg="white", width=15,
                 command=lambda: self.save_receipt_to_file(receipt_content)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close Receipt", bg="#999999", fg="white", width=15,
                 command=receipt_window.destroy).pack(side=tk.LEFT, padx=5)
        
        # Center the receipt window
        receipt_window.transient(self.root)
        receipt_window.grab_set()
        receipt_window.update_idletasks()
        width = receipt_window.winfo_width()
        height = receipt_window.winfo_height()
        x = (receipt_window.winfo_screenwidth() // 2) - (width // 2)
        y = (receipt_window.winfo_screenheight() // 2) - (height // 2)
        receipt_window.geometry(f'{width}x{height}+{x}+{y}')
    
    def save_receipt_to_file(self, receipt_text, auto_save=False):
        """Save receipt to a text file in receipts directory"""
        # Create receipts folder if it doesn't exist
        receipts_dir = "receipts"
        if not os.path.exists(receipts_dir):
            os.makedirs(receipts_dir)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{receipts_dir}/receipt_{timestamp}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(receipt_text)
            
            if not auto_save:  # Only show message if manually printed
                messagebox.showinfo("Success", f"Receipt saved to:\n{filename}")
            return filename
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save receipt: {str(e)}")
            return None
    
    def update_cart_display(self):
        # Clear existing items
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add cart items
        for item in self.pos_functions.get_cart_items():
            self.cart_tree.insert("", tk.END, values=(
                item["product"],
                f"₱{item['price']:.2f}",
                item["quantity"],
                f"₱{item['total']:.2f}"
            ))
        
        # Update totals
        subtotal = self.pos_functions.calculate_subtotal()
        grand_total = self.pos_functions.calculate_grand_total()
        self.total_label.config(text=f"Total: ₱{subtotal:.2f}")
        self.grand_total_label.config(text=f"Grand Total (incl. tax): ₱{grand_total:.2f}")
    
    def open_product_management(self):
        ProductManagementWindow(self.root, self.product_manager, self)

class ProductManagementWindow:
    def __init__(self, parent, product_manager, main_window):
        self.window = tk.Toplevel(parent)
        self.window.title("Product Management")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        self.product_manager = product_manager
        self.main_window = main_window
        
        self.setup_window()
        self.load_products()
    
    def setup_window(self):
        # Product table
        table_frame = tk.Frame(self.window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        columns = ("Product Name", "Price", "Stock Quantity")
        self.product_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.product_tree.heading("Product Name", text="Product Name")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Stock Quantity", text="Stock Quantity")
        self.product_tree.column("Product Name", width=200, anchor="w")
        self.product_tree.column("Price", width=150, anchor="center")
        self.product_tree.column("Stock Quantity", width=150, anchor="center")
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        self.product_tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Input frame
        input_frame = tk.Frame(self.window, bg="white")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(input_frame, text="Product Name:", bg="white").grid(row=0, column=0, sticky="w", padx=5)
        self.name_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.name_var, width=20).grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Price:", bg="white").grid(row=0, column=2, sticky="w", padx=5)
        self.price_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.price_var, width=15).grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="Stock Qty:", bg="white").grid(row=0, column=4, sticky="w", padx=5)
        self.stock_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.stock_var, width=15).grid(row=0, column=5, padx=5)
        
        # Button frame
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(btn_frame, text="Add Product", bg="#5cb85c", fg="white", 
                 command=self.add_product).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Update Product", bg="#5bc0de", fg="white", 
                 command=self.update_product).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Product", bg="#d9534f", fg="white", 
                 command=self.delete_product).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", bg="#999999", fg="white", 
                 command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def load_products(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        for name, price, stock in self.product_manager.get_all_products():
            self.product_tree.insert("", tk.END, values=(name, f"₱{price:.2f}", stock))
    
    def on_select(self, event):
        selected = self.product_tree.selection()
        if selected:
            values = self.product_tree.item(selected[0])["values"]
            self.name_var.set(values[0])
            self.price_var.set(values[1].replace("₱", ""))
            self.stock_var.set(values[2])
    
    def add_product(self):
        try:
            name = self.name_var.get().strip()
            price = float(self.price_var.get())
            stock = int(self.stock_var.get())
            
            if not name:
                raise ValueError("Product name cannot be empty")
            
            self.product_manager.add_product(name, price, stock)
            self.load_products()
            self.clear_inputs()
            self.main_window.product_combo['values'] = self.product_manager.get_product_names()
            messagebox.showinfo("Success", "Product added successfully")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def update_product(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product to update")
            return
        
        try:
            name = self.name_var.get().strip()
            price = float(self.price_var.get())
            stock = int(self.stock_var.get())
            
            self.product_manager.update_product(name, price, stock)
            self.load_products()
            self.clear_inputs()
            self.main_window.product_combo['values'] = self.product_manager.get_product_names()
            messagebox.showinfo("Success", "Product updated successfully")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def delete_product(self):
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a product to delete")
            return
        
        name = self.product_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete product '{name}'?"):
            self.product_manager.delete_product(name)
            self.load_products()
            self.clear_inputs()
            self.main_window.product_combo['values'] = self.product_manager.get_product_names()
            messagebox.showinfo("Success", "Product deleted successfully")
    
    def clear_inputs(self):
        self.name_var.set("")
        self.price_var.set("")
        self.stock_var.set("")