from abc import ABC, abstractmethod
from typing import List
from database.ProductDatabase import ProductDatabase
from entities.Product import Product

# Patrón Singleton para el Carrito de Compras
class ShoppingCart:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ShoppingCart, cls).__new__(cls)
            cls._instance.products = []
        return cls._instance

    def get_products(self):
        return self.products  
    
    def add_product(self, product):
        self.products.append(product)

    def checkout(self):
        total_cost = sum([product.price for product in self.products])
        print(f"Total a pagar: {total_cost}")


# Patrón Strategy para la búsqueda de productos
class ProductSearchStrategy(ABC):
    @abstractmethod
    def search_products(self, query) -> List[str]:
        pass

class OnlineProductSearch(ProductSearchStrategy):
    def __init__(self, product_database: ProductDatabase):
        self.product_database = product_database

    def search_products(self, query) -> List[Product]:
        all_products = self.product_database.get_all_products()
        matching_products = [product for product in all_products if query.lower() in product.name.lower()]

        return matching_products

# Patrón Command para gestionar pedidos
class OrderCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

# Comando concreto para realizar pedidos
class PlaceOrderCommand(OrderCommand):
    def __init__(self, cart):
        self.cart = cart

    def execute(self):
        print("Pedido realizado con éxito")



if __name__ == "__main__":
    # Crear instancia de la base de datos de productos
    product_database = ProductDatabase()

    # Crear instancia del carrito de compras (Singleton)
    cart = ShoppingCart()

    # Realizar búsqueda de productos (Strategy)
    search_strategy = OnlineProductSearch(product_database)
    print("Resultados de la búsqueda:")
    cart.add_product(search_strategy.search_products("leche deslactosada")[0])
    cart.add_product(search_strategy.search_products("pan integral")[0])
    cart.add_product(search_strategy.search_products("aceite de oliva")[0])

    # Mostrar productos en el carrito
    print("Productos en el carrito:")
    for product in cart.get_products():
        print(f"Nombre: {product.name}, Precio: {product.price}")

    # Realizar pedido (Command)
    place_order_command = PlaceOrderCommand(cart)
    place_order_command.execute()

    # Proceso de pago
    cart.checkout()