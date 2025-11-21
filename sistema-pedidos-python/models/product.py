"""
Model Product - Programação Orientada a Objetos
Representa um produto do sistema
"""

from utils.database import db


class Product:
    """Classe que representa um produto"""
    
    def __init__(self, id=None, nome=None, descricao=None, preco=None, 
                 estoque=0, ativo=True, imagem_url=None, categoria=None,
                 created_at=None, updated_at=None):
        """
        Inicializa objeto Product
        
        Args:
            id (int): ID do produto
            nome (str): Nome do produto
            descricao (str): Descrição
            preco (int): Preço em centavos
            estoque (int): Quantidade em estoque
            ativo (bool): Produto ativo/inativo
            imagem_url (str): URL da imagem
            categoria (str): Categoria do produto
            created_at (datetime): Data de criação
            updated_at (datetime): Data de atualização
        """
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.ativo = ativo
        self.imagem_url = imagem_url
        self.categoria = categoria
        self.created_at = created_at
        self.updated_at = updated_at
    
    def validar(self):
        """
        Valida dados do produto
        
        Returns:
            tuple: (bool, dict) - (é_válido, dicionário_de_erros)
        """
        erros = {}
        
        # Estrutura de decisão: valida nome
        if not self.nome or len(self.nome.strip()) < 3:
            erros['nome'] = 'Nome deve ter pelo menos 3 caracteres'
        
        # Estrutura de decisão: valida preço
        if not self.preco or self.preco <= 0:
            erros['preco'] = 'Preço deve ser maior que zero'
        
        # Estrutura de decisão: valida estoque
        if self.estoque < 0:
            erros['estoque'] = 'Estoque não pode ser negativo'
        
        if erros:
            return False, erros
        else:
            return True, {}
    
    def salvar(self):
        """
        Salva produto no banco de dados
        
        Returns:
            int: ID do produto criado
        
        Raises:
            Exception: Se houver erro ao salvar
        """
        # Try/Except para tratamento de exceções
        try:
            # Valida dados antes de salvar
            valido, erros = self.validar()
            if not valido:
                raise ValueError(f"Dados inválidos: {erros}")
            
            query = """
                INSERT INTO products (nome, descricao, preco, estoque, ativo, imagem_url, categoria)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.nome, self.descricao, self.preco, self.estoque, 
                     self.ativo, self.imagem_url, self.categoria)
            
            self.id = db.execute_query(query, params)
            return self.id
        
        except Exception as e:
            print(f"❌ Erro ao salvar produto: {e}")
            raise e
    
    def atualizar(self):
        """
        Atualiza dados do produto no banco
        
        Returns:
            int: Número de linhas afetadas
        
        Raises:
            Exception: Se houver erro ao atualizar
        """
        try:
            # Valida dados antes de atualizar
            valido, erros = self.validar()
            if not valido:
                raise ValueError(f"Dados inválidos: {erros}")
            
            query = """
                UPDATE products 
                SET nome=%s, descricao=%s, preco=%s, estoque=%s, ativo=%s, imagem_url=%s, categoria=%s
                WHERE id=%s
            """
            params = (self.nome, self.descricao, self.preco, self.estoque, 
                     self.ativo, self.imagem_url, self.categoria, self.id)
            
            return db.execute_query(query, params)
        
        except Exception as e:
            print(f"❌ Erro ao atualizar produto: {e}")
            raise e
    
    def deletar(self):
        """
        Soft delete - marca produto como inativo
        
        Returns:
            int: Número de linhas afetadas
        """
        try:
            query = "UPDATE products SET ativo = FALSE WHERE id = %s"
            return db.execute_query(query, (self.id,))
        
        except Exception as e:
            print(f"❌ Erro ao deletar produto: {e}")
            raise e
    
    @staticmethod
    def buscar_por_id(product_id):
        """
        Busca produto por ID
        
        Args:
            product_id (int): ID do produto
        
        Returns:
            Product: Objeto Product ou None
        """
        query = "SELECT * FROM products WHERE id = %s"
        result = db.fetch_one(query, (product_id,))
        
        if result:
            return Product(**result)
        return None
    
    @staticmethod
    def listar_ativos():
        """
        Lista produtos ativos
        
        Returns:
            list: Lista de objetos Product
        """
        query = "SELECT * FROM products WHERE ativo = TRUE ORDER BY created_at DESC"
        results = db.fetch_all(query)
        
        return [Product(**row) for row in results]
    
    @staticmethod
    def listar_todos():
        """
        Lista todos os produtos (incluindo inativos)
        
        Returns:
            list: Lista de objetos Product
        """
        query = "SELECT * FROM products ORDER BY created_at DESC"
        results = db.fetch_all(query)
        
        return [Product(**row) for row in results]
    
    def to_dict(self):
        """
        Converte objeto para dicionário
        
        Returns:
            dict: Representação em dicionário
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'estoque': self.estoque,
            'ativo': self.ativo,
            'imagem_url': self.imagem_url,
            'categoria': self.categoria,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
