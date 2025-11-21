"""
Módulo de conexão com banco de dados MySQL
"""

import mysql.connector
from mysql.connector import Error
import os


class Database:
    """Classe para gerenciar conexão com banco de dados MySQL"""
    
    def __init__(self):
        """Inicializa conexão com banco de dados"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'sistema_pedidos')
            )
            
            if self.connection.is_connected():
                print("✅ Conexão com MySQL estabelecida com sucesso")
        
        except Error as e:
            print(f"❌ Erro ao conectar ao MySQL: {e}")
            self.connection = None
    
    def execute_query(self, query, params=None):
        """
        Executa query de modificação (INSERT, UPDATE, DELETE)
        
        Args:
            query (str): Query SQL
            params (tuple): Parâmetros da query
        
        Returns:
            int: ID do último registro inserido ou número de linhas afetadas
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            
            # Retorna ID do último insert ou número de linhas afetadas
            if cursor.lastrowid:
                return cursor.lastrowid
            return cursor.rowcount
        
        except Error as e:
            print(f"❌ Erro ao executar query: {e}")
            self.connection.rollback()
            raise e
        
        finally:
            if cursor:
                cursor.close()
    
    def fetch_one(self, query, params=None):
        """
        Executa query de seleção e retorna um registro
        
        Args:
            query (str): Query SQL
            params (tuple): Parâmetros da query
        
        Returns:
            dict: Registro encontrado ou None
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        
        except Error as e:
            print(f"❌ Erro ao buscar registro: {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()
    
    def fetch_all(self, query, params=None):
        """
        Executa query de seleção e retorna todos os registros
        
        Args:
            query (str): Query SQL
            params (tuple): Parâmetros da query
        
        Returns:
            list: Lista de registros encontrados
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results
        
        except Error as e:
            print(f"❌ Erro ao buscar registros: {e}")
            return []
        
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """Fecha conexão com o banco de dados"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✅ Conexão com MySQL fechada")


# Instância global do banco de dados
db = Database()
