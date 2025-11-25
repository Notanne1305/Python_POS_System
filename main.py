from products import show_products
from functions import select_product, compute_total, generate_receipt

print("=== WELCOME TO PYTHON POS ===\n")
show_products()
product = select_product()
if product:
    try:
        quantity = int(input(f"Enter quantity for {product['Product']}: "))
    except (ValueError, KeyError):
        print("Invalid input or product data. Exiting.")
    else:
        subtotal, tax, total = compute_total(product['price'], quantity)
        generate_receipt(product, quantity, subtotal, tax, total)