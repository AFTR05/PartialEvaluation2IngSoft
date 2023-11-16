from entities.Product import Product

class ProductDatabase:
    def __init__(self):
        self.products = [
            Product("leche deslactosada", 5000.0),
            Product("pan integral", 10000.0),
            Product("arequipe", 5000.0),
            Product("frijoles", 7000.0),
            Product("lentejas", 6000.0),
            Product("maiz pira", 3000.0),
            Product("aceite de oliva", 25000.0),
            Product("Yogurt", 15000.0),
            Product("Galletas saltin", 7000.0),
            Product("Chocolisto", 20000.0)
        ]

    def get_all_products(self):
        return self.products