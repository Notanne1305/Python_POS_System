"""
Products module - Handles product data storage and management
"""

class ProductManager:
    def __init__(self):
        self.products = {
            "Apple": {"price": 15.00, "stock": 50},
            "Banana": {"price": 10.00, "stock": 30},
            "Bread": {"price": 45.99, "stock": 25},
            "Eggs": {"price": 11.00, "stock": 40},
            "Hotdog": {"price": 45.00, "stock": 42},
            "Milk": {"price": 25.49, "stock": 20}
        }
    
    def get_all_products(self):
        """Return all products as a list of tuples"""
        return [(name, data["price"], data["stock"]) 
                for name, data in self.products.items()]
    
    def get_product(self, name):
        """Get a specific product by name"""
        return self.products.get(name)
    
    def add_product(self, name, price, stock):
        """Add a new product"""
        self.products[name] = {"price": float(price), "stock": int(stock)}
    
    def update_product(self, name, price, stock):
        """Update existing product"""
        if name in self.products:
            self.products[name] = {"price": float(price), "stock": int(stock)}
            return True
        return False
    
    def delete_product(self, name):
        """Delete a product"""
        if name in self.products:
            del self.products[name]
            return True
        return False
    
    def get_product_names(self):
        """Return list of product names"""
        return list(self.products.keys())
    
    def reduce_stock(self, name, quantity):
        """Reduce stock when item is purchased"""
        if name in self.products:
            self.products[name]["stock"] -= quantity