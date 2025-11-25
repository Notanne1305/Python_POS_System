products = {
    1: {"Product": "Burger", "price": 50},
    2: {"Product": "Fries", "price": 30},
    3: {"Product": "Spaghetti", "price": 50},
}

def show_products():
    print("Available Product:")
    for code, info in products.items():
        print(f"{code}. {info['Product']} - ₱{info['price']:.2f} ")