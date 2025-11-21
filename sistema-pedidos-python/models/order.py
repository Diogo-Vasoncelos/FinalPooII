"""
Model Order - Programação Orientada a Objetos
Representa um pedido do sistema
"""

from utils.database import db


class Order:
    """Classe que representa um pedido"""
    
    def __init__(self, id=None, user_id=None, status='pendente', valor_total=0,
                 observacoes=None, endereco_entrega=None, created_at=None, updated_at=None):
        """
        Inicializa objeto Order
        
        Args:
            id (int): ID do pedido
            user_id (int): ID do usuário
            status (str): Status do pedido
            valor_total (int): Valor total em centavos
            observacoes (str): Observações
            endereco_entrega (str): Endereço de entrega
            created_at (datetime): Data de criação
            updated_at (datetime): Data de atualização
        """
        self.id = id
        self.user_id = user_id
        self.status = status
        self.valor_total = valor_total
        self.observacoes = observacoes
        self.endereco_entrega = endereco_entrega
        self.created_at = created_at
        self.updated_at = updated_at
        self.items = []  # Lista de OrderItem
    
    def salvar(self):
        """
        Salva pedido no banco de dados
        
        Returns:
            int: ID do pedido criado
        """
        try:
            query = """
                INSERT INTO orders (user_id, status, valor_total, observacoes, endereco_entrega)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (self.user_id, self.status, self.valor_total, 
                     self.observacoes, self.endereco_entrega)
            
            self.id = db.execute_query(query, params)
            return self.id
        
        except Exception as e:
            print(f"❌ Erro ao salvar pedido: {e}")
            raise e
    
    def atualizar_status(self, novo_status):
        """
        Atualiza status do pedido
        
        Args:
            novo_status (str): Novo status
        
        Returns:
            int: Número de linhas afetadas
        """
        try:
            query = "UPDATE orders SET status = %s WHERE id = %s"
            self.status = novo_status
            return db.execute_query(query, (novo_status, self.id))
        
        except Exception as e:
            print(f"❌ Erro ao atualizar status: {e}")
            raise e
    
    @staticmethod
    def buscar_por_id(order_id):
        """
        Busca pedido por ID
        
        Args:
            order_id (int): ID do pedido
        
        Returns:
            Order: Objeto Order ou None
        """
        query = "SELECT * FROM orders WHERE id = %s"
        result = db.fetch_one(query, (order_id,))
        
        if result:
            order = Order(**result)
            # Busca itens do pedido
            order.items = OrderItem.buscar_por_pedido(order_id)
            return order
        return None
    
    @staticmethod
    def buscar_por_usuario(user_id):
        """
        Busca pedidos de um usuário
        
        Args:
            user_id (int): ID do usuário
        
        Returns:
            list: Lista de objetos Order
        """
        query = "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC"
        results = db.fetch_all(query, (user_id,))
        
        return [Order(**row) for row in results]
    
    @staticmethod
    def listar_todos():
        """
        Lista todos os pedidos
        
        Returns:
            list: Lista de objetos Order
        """
        query = "SELECT * FROM orders ORDER BY created_at DESC"
        results = db.fetch_all(query)
        
        return [Order(**row) for row in results]
    
    def to_dict(self):
        """
        Converte objeto para dicionário
        
        Returns:
            dict: Representação em dicionário
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'valor_total': self.valor_total,
            'observacoes': self.observacoes,
            'endereco_entrega': self.endereco_entrega,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None,
            'items': [item.to_dict() for item in self.items]
        }


class OrderItem:
    """Classe que representa um item do pedido"""
    
    def __init__(self, id=None, order_id=None, product_id=None, quantidade=0,
                 preco_unitario=0, subtotal=0, created_at=None):
        """
        Inicializa objeto OrderItem
        
        Args:
            id (int): ID do item
            order_id (int): ID do pedido
            product_id (int): ID do produto
            quantidade (int): Quantidade
            preco_unitario (int): Preço unitário em centavos
            subtotal (int): Subtotal em centavos
            created_at (datetime): Data de criação
        """
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = subtotal
        self.created_at = created_at
    
    def salvar(self):
        """
        Salva item do pedido no banco
        
        Returns:
            int: ID do item criado
        """
        try:
            query = """
                INSERT INTO order_items (order_id, product_id, quantidade, preco_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (self.order_id, self.product_id, self.quantidade, 
                     self.preco_unitario, self.subtotal)
            
            self.id = db.execute_query(query, params)
            return self.id
        
        except Exception as e:
            print(f"❌ Erro ao salvar item do pedido: {e}")
            raise e
    
    @staticmethod
    def buscar_por_pedido(order_id):
        """
        Busca itens de um pedido
        
        Args:
            order_id (int): ID do pedido
        
        Returns:
            list: Lista de objetos OrderItem
        """
        query = "SELECT * FROM order_items WHERE order_id = %s"
        results = db.fetch_all(query, (order_id,))
        
        return [OrderItem(**row) for row in results]
    
    def to_dict(self):
        """
        Converte objeto para dicionário
        
        Returns:
            dict: Representação em dicionário
        """
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'subtotal': self.subtotal,
            'created_at': str(self.created_at) if self.created_at else None
        }
