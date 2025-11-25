from products import products

VAT_RATE = 0.12

def select_product():
    try:
        choice = int(input("Enter product number: "))
        if choice in products: 
            return products[choice]
        else:
            print("Invalid product selected. Please choose a valid number.")
    except Exception as e:
        print("An unexpected error occured: {e}")
        return None

def compute_total(price, quantity):
    subtotal = price * quantity
    tax = subtotal * VAT_RATE
    total = subtotal + tax
    return subtotal, tax, total

def generate_receipt(product, quantity, subtotal, tax, total):
    print("\n===== RECEIPT =====")
    print(f"Product: {product['Product']}")
    print(f"Unit Price: ₱{product['price']:.2f}")
    print(f"Quantity: {quantity}")
    print(f"Subtotal: ₱{subtotal:.2f}")
    print(f"VAT (12%): ₱{tax:.2f}")
    print(f"TOTAL: ₱{total:.2f}")
    print("====================")
    print("Thank you for your purchase!")