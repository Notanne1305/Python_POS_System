"""
Functions module - Business logic for POS operations
"""

class POSFunctions:
    def __init__(self, product_manager):
        self.product_manager = product_manager
        self.cart = []
    
    def add_to_cart(self, product_name, quantity):
        """Add item to cart"""
        product = self.product_manager.get_product(product_name)
        if product:
            price = product["price"]
            total = price * quantity
            self.cart.append({
                "product": product_name,
                "price": price,
                "quantity": quantity,
                "total": total
            })
            return True
        return False
    
    def update_cart_item(self, index, quantity):
        """Update quantity of item in cart"""
        if 0 <= index < len(self.cart):
            self.cart[index]["quantity"] = quantity
            self.cart[index]["total"] = self.cart[index]["price"] * quantity
            return True
        return False
    
    def delete_cart_item(self, index):
        """Remove item from cart"""
        if 0 <= index < len(self.cart):
            self.cart.pop(index)
            return True
        return False
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.cart.clear()
    
    def get_cart_items(self):
        """Return all cart items"""
        return self.cart
    
    def calculate_subtotal(self):
        """Calculate subtotal of all items in cart"""
        return sum(item["total"] for item in self.cart)
    
    def calculate_tax(self, tax_rate=0.12):
        """Calculate tax (12% VAT)"""
        return self.calculate_subtotal() * tax_rate
    
    def calculate_grand_total(self):
        """Calculate grand total including tax"""
        return self.calculate_subtotal() + self.calculate_tax()
    
    def complete_purchase(self):
        """Complete the purchase and update stock"""
        for item in self.cart:
            self.product_manager.reduce_stock(item["product"], item["quantity"])
        self.clear_cart()
        return True