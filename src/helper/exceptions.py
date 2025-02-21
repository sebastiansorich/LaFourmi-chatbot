# exceptions.py

class InsufficientStockError(Exception):
    def __init__(self, product_id, description, message="Stock insuficiente"):
        self.product_id = product_id
        self.message = f"{message} para el producto {product_id} {description}"
        super().__init__(self.message)
class UnauthorizedError(Exception):
    def __init__(self, client_id, description, message="El código de pedido no esta vinculado al número de celular"):
        self.client_id = client_id
        self.message = f"{message} para el cliente {description}"
        super().__init__(self.message)
class DataProcessedError(Exception):
    def __init__(self, order_id, status):
        self.description = ""
        if status == 2:
            self.description = "ya esta procesado, comuniquese con la oficina central si desea cancelar este pedido."
        if  status == 3:
            self.description = "se encuentra cancelado"
        self.message = f"El pedido con código: {order_id} {self.description} "
        super().__init__(self.message)