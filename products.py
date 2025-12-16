products = {
    1: {"Product": "Burger", "price": 50},
    2: {"Product": "Fries", "price": 30},
    3: {"Product": "Spaghetti", "price": 50},
    4: {"Product": "1-pc Chicken with Rice", "price": 89},
    5: {"Product": "Hotdog Sandwich", "price": 35},
    6: {"Product": "Regular Coke", "price": 25},
    7: {"Product": "Iced Tea", "price": 30},
    8: {"Product": "Milkshake", "price": 55},
    9: {"Product": "Ice Cream Sundae", "price": 35},
    10: {"Product": "Brownie", "price": 25},
    
}

def show_products():
    print("Available Product:")
    for code, info in products.items():
        print(f"{code}. {info['Product']} - ₱{info['price']:.2f} ")