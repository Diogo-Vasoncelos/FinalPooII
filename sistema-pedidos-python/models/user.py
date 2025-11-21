"""
Model User - Programação Orientada a Objetos
Representa um usuário do sistema
"""

from werkzeug.security import generate_password_hash, check_password_hash
from utils.database import db
from utils.validations import validar_cpf, validar_email, validar_telefone, validar_idade, validar_nome, validar_endereco, formatar_cpf, formatar_telefone


class User:
    """Classe que representa um usuário do sistema"""
    
    def __init__(self, id=None, nome=None, email=None, senha=None, cpf=None, 
                 telefone=None, idade=None, endereco=None, role='user', 
                 created_at=None, updated_at=None):
        """
        Inicializa objeto User
        
        Args:
            id (int): ID do usuário
            nome (str): Nome completo
            email (str): Email
            senha (str): Senha (será hasheada)
            cpf (str): CPF
            telefone (str): Telefone
            idade (int): Idade
            endereco (str): Endereço completo
            role (str): Tipo de usuário ('user' ou 'admin')
            created_at (datetime): Data de criação
            updated_at (datetime): Data de atualização
        """
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.telefone = telefone
        self.idade = idade
        self.endereco = endereco
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
    
    def validar(self):
        """
        Valida dados do usuário usando estruturas de decisão
        
        Returns:
            tuple: (bool, dict) - (é_válido, dicionário_de_erros)
        """
        erros = {}
        
        # Valida nome
        valido, mensagem = validar_nome(self.nome)
        if not valido:
            erros['nome'] = mensagem
        
        # Valida email
        valido, mensagem = validar_email(self.email)
        if not valido:
            erros['email'] = mensagem
        
        # Valida CPF
        valido, mensagem = validar_cpf(self.cpf)
        if not valido:
            erros['cpf'] = mensagem
        
        # Valida telefone
        valido, mensagem = validar_telefone(self.telefone)
        if not valido:
            erros['telefone'] = mensagem
        
        # Valida idade
        valido, mensagem = validar_idade(self.idade)
        if not valido:
            erros['idade'] = mensagem
        
        # Valida endereço
        valido, mensagem = validar_endereco(self.endereco)
        if not valido:
            erros['endereco'] = mensagem
        
        # Valida senha
        if not self.senha or len(self.senha) < 6:
            erros['senha'] = 'Senha deve ter pelo menos 6 caracteres'
        
        # Estrutura de decisão: retorna resultado da validação
        if erros:
            return False, erros
        else:
            return True, {}
    
    def set_senha(self, senha):
        """
        Define senha hasheada
        
        Args:
            senha (str): Senha em texto plano
        """
        self.senha = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        """
        Verifica se senha está correta
        
        Args:
            senha (str): Senha em texto plano
        
        Returns:
            bool: True se senha está correta
        """
        return check_password_hash(self.senha, senha)
    
    def salvar(self):
        """
        Salva usuário no banco de dados
        
        Returns:
            int: ID do usuário criado
        
        Raises:
            Exception: Se houver erro ao salvar
        """
        # Try/Except para tratamento de exceções
        try:
            # Valida dados antes de salvar
            valido, erros = self.validar()
            if not valido:
                raise ValueError(f"Dados inválidos: {erros}")
            
            # Formata CPF e telefone
            self.cpf = formatar_cpf(self.cpf)
            self.telefone = formatar_telefone(self.telefone)
            
            # Verifica se email já existe
            if self.email_existe():
                raise ValueError("Email já cadastrado")
            
            # Verifica se CPF já existe
            if self.cpf_existe():
                raise ValueError("CPF já cadastrado")
            
            # Hasheia senha se ainda não foi hasheada
            if not self.senha.startswith('pbkdf2:sha256:'):
                self.set_senha(self.senha)
            
            # Insere no banco
            query = """
                INSERT INTO users (nome, email, senha, cpf, telefone, idade, endereco, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (self.nome, self.email, self.senha, self.cpf, self.telefone, 
                     self.idade, self.endereco, self.role)
            
            self.id = db.execute_query(query, params)
            return self.id
        
        except Exception as e:
            print(f"❌ Erro ao salvar usuário: {e}")
            raise e
    
    def atualizar(self):
        """
        Atualiza dados do usuário no banco
        
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
            
            # Formata CPF e telefone
            self.cpf = formatar_cpf(self.cpf)
            self.telefone = formatar_telefone(self.telefone)
            
            query = """
                UPDATE users 
                SET nome=%s, email=%s, cpf=%s, telefone=%s, idade=%s, endereco=%s, role=%s
                WHERE id=%s
            """
            params = (self.nome, self.email, self.cpf, self.telefone, 
                     self.idade, self.endereco, self.role, self.id)
            
            return db.execute_query(query, params)
        
        except Exception as e:
            print(f"❌ Erro ao atualizar usuário: {e}")
            raise e
    
    def email_existe(self):
        """
        Verifica se email já existe no banco
        
        Returns:
            bool: True se email existe
        """
        query = "SELECT id FROM users WHERE email = %s"
        result = db.fetch_one(query, (self.email,))
        
        # Estrutura de decisão: retorna True se encontrou registro
        if result and (not self.id or result['id'] != self.id):
            return True
        return False
    
    def cpf_existe(self):
        """
        Verifica se CPF já existe no banco
        
        Returns:
            bool: True se CPF existe
        """
        cpf_formatado = formatar_cpf(self.cpf)
        query = "SELECT id FROM users WHERE cpf = %s"
        result = db.fetch_one(query, (cpf_formatado,))
        
        # Estrutura de decisão: retorna True se encontrou registro
        if result and (not self.id or result['id'] != self.id):
            return True
        return False
    
    @staticmethod
    def buscar_por_id(user_id):
        """
        Busca usuário por ID
        
        Args:
            user_id (int): ID do usuário
        
        Returns:
            User: Objeto User ou None
        """
        query = "SELECT * FROM users WHERE id = %s"
        result = db.fetch_one(query, (user_id,))
        
        if result:
            return User(**result)
        return None
    
    @staticmethod
    def buscar_por_email(email):
        """
        Busca usuário por email
        
        Args:
            email (str): Email do usuário
        
        Returns:
            User: Objeto User ou None
        """
        query = "SELECT * FROM users WHERE email = %s"
        result = db.fetch_one(query, (email,))
        
        if result:
            return User(**result)
        return None
    
    @staticmethod
    def listar_todos():
        """
        Lista todos os usuários
        
        Returns:
            list: Lista de objetos User
        """
        query = "SELECT * FROM users ORDER BY created_at DESC"
        results = db.fetch_all(query)
        
        return [User(**row) for row in results]
    
    def to_dict(self):
        """
        Converte objeto para dicionário
        
        Returns:
            dict: Representação em dicionário
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'idade': self.idade,
            'endereco': self.endereco,
            'role': self.role,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None
        }
