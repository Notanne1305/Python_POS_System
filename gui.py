import tkinter as tk
from tkinter import ttk, messagebox
from functions import compute_total
from products import products


class POSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python POS System")
        self.root.geometry("400x350")

        ttk.Label(root, text="Select Product:", font=("Arial", 12)).pack(pady=5)

        self.product_var = tk.StringVar()
        self.product_dropdown = ttk.Combobox(
            root,
            textvariable=self.product_var,
            state="readonly",
            width=30,
            font=("Arial", 11)
        )
        self.product_dropdown.pack()

        self.product_list = list(products.values())
        product_names = [f"{p['Product']} - ₱{p['price']:.2f}" for p in self.product_list]
        self.product_dropdown['values'] = product_names

        ttk.Label(root, text="Enter Quantity:", font=("Arial", 12)).pack(pady=5)
        self.quantity_entry = ttk.Entry(root, width=32, font=("Arial", 11))
        self.quantity_entry.pack()

        ttk.Button(
            root,
            text="Compute Total",
            command=self.compute,
            width=39,                 
            ).pack(pady=20, ipadx=10, ipady=6)

        self.result_label = ttk.Label(root, text="", font=("Arial", 11))
        self.result_label.pack(pady=10)

        ttk.Button(
            root, 
            text="Generate Receipt", 
            command=self.show_receipt,
            width=39,
            ).pack(pady=10, ipadx=10, ipady=6
            )

        self.selected_product = None
        self.subtotal = 0
        self.tax = 0
        self.total = 0

    def compute(self):
        try:
            selected_index = self.product_dropdown.current()
            if selected_index == -1:
                messagebox.showerror("Error", "Please select a product.")
                return

            self.selected_product = self.product_list[selected_index]

            quantity = int(self.quantity_entry.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be a positive integer.")
                return

            price = self.selected_product['price']
            self.subtotal, self.tax, self.total = compute_total(price, quantity)

            self.result_label.config(
                text=f"Subtotal: ₱{self.subtotal:.2f}\nVAT: ₱{self.tax:.2f}\nTotal: ₱{self.total:.2f}"
            )

        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Enter a number.")
            return

    def show_receipt(self):
        if not self.selected_product:
            messagebox.showerror("Error", "Compute total first.")
            return

        receipt_window = tk.Toplevel()
        receipt_window.title("Receipt")
        receipt_window.geometry("300x300")

        receipt_text = (
            f"====== RECEIPT ======\n"
            f"Product: {self.selected_product['Product']}\n"
            f"Unit Price: ₱{self.selected_product['price']:.2f}\n"
            f"Subtotal: ₱{self.subtotal:.2f}\n"
            f"VAT (12%): ₱{self.tax:.2f}\n"
            f"TOTAL: ₱{self.total:.2f}\n"
            f"=====================\n"
            f"Thank you!"
        )

        tk.Label(
            receipt_window,
            text=receipt_text,
            font=("Consolas", 11),
            justify="left"
        ).pack(padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = POSApp(root)
    root.mainloop()
