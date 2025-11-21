"""
Sistema de Pedidos Online - POO II
Aplicação Flask com autenticação, validações e controle de sessões
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_session import Session
from werkzeug.security import check_password_hash
from functools import wraps
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importa models
from models.user import User
from models.product import Product
from models.order import Order, OrderItem
from utils.validations import formatar_preco

# Inicializa Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-desenvolvimento')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


# ==================== DECORATORS ====================

def login_required(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator para rotas que requerem permissão de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login para acessar esta página', 'error')
            return redirect(url_for('login'))
        
        user = User.buscar_por_id(session['user_id'])
        if not user or user.role != 'admin':
            flash('Acesso negado. Apenas administradores podem acessar esta página', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROTAS PÚBLICAS ====================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            senha = request.form.get('senha')
            
            # Estrutura de decisão: valida campos
            if not email or not senha:
                flash('Email e senha são obrigatórios', 'error')
                return render_template('login.html')
            
            # Busca usuário por email
            user = User.buscar_por_email(email)
            
            # Estrutura de decisão: verifica se usuário existe e senha está correta
            if user and user.verificar_senha(senha):
                # Cria sessão
                session['user_id'] = user.id
                session['user_name'] = user.nome
                session['user_role'] = user.role
                
                flash(f'Bem-vindo, {user.nome}!', 'success')
                
                # Redireciona baseado no role
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('cliente_dashboard'))
            else:
                flash('Email ou senha incorretos', 'error')
        
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            flash('Erro ao fazer login. Tente novamente', 'error')
    
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """Página de cadastro"""
    if request.method == 'POST':
        try:
            # Try/Except para tratamento de exceções
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')
            cpf = request.form.get('cpf')
            telefone = request.form.get('telefone')
            idade = request.form.get('idade')
            endereco = request.form.get('endereco')
            
            # Cria objeto User
            user = User(
                nome=nome,
                email=email,
                senha=senha,
                cpf=cpf,
                telefone=telefone,
                idade=int(idade),
                endereco=endereco,
                role='user'
            )
            
            # Valida e salva
            user.salvar()
            
            flash('Cadastro realizado com sucesso! Faça login para continuar', 'success')
            return redirect(url_for('login'))
        
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            print(f"❌ Erro no cadastro: {e}")
            flash('Erro ao realizar cadastro. Tente novamente', 'error')
    
    return render_template('cadastro.html')


@app.route('/logout')
def logout():
    """Logout - limpa sessão"""
    session.clear()
    flash('Você saiu do sistema', 'info')
    return redirect(url_for('index'))


# ==================== ROTAS DO CLIENTE ====================

@app.route('/cliente/dashboard')
@login_required
def cliente_dashboard():
    """Dashboard do cliente"""
    try:
        user = User.buscar_por_id(session['user_id'])
        pedidos = Order.buscar_por_usuario(user.id)
        
        # Estatísticas
        total_pedidos = len(pedidos)
        pedidos_entregues = len([p for p in pedidos if p.status == 'entregue'])
        pedidos_pendentes = len([p for p in pedidos if p.status in ['pendente', 'processando']])
        
        return render_template('cliente_dashboard.html',
                             user=user,
                             pedidos=pedidos,
                             total_pedidos=total_pedidos,
                             pedidos_entregues=pedidos_entregues,
                             pedidos_pendentes=pedidos_pendentes,
                             formatar_preco=formatar_preco)
    
    except Exception as e:
        print(f"❌ Erro ao carregar dashboard: {e}")
        flash('Erro ao carregar dashboard', 'error')
        return redirect(url_for('index'))


# ==================== ROTAS DO ADMIN ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Dashboard administrativo"""
    try:
        produtos = Product.listar_todos()
        pedidos = Order.listar_todos()
        usuarios = User.listar_todos()
        
        # Estatísticas
        total_pedidos = len(pedidos)
        receita_total = sum(p.valor_total for p in pedidos)
        produtos_ativos = len([p for p in produtos if p.ativo])
        total_clientes = len(usuarios)
        
        return render_template('admin_dashboard.html',
                             produtos=produtos,
                             pedidos=pedidos,
                             usuarios=usuarios,
                             total_pedidos=total_pedidos,
                             receita_total=receita_total,
                             produtos_ativos=produtos_ativos,
                             total_clientes=total_clientes,
                             formatar_preco=formatar_preco)
    
    except Exception as e:
        print(f"❌ Erro ao carregar dashboard admin: {e}")
        flash('Erro ao carregar dashboard', 'error')
        return redirect(url_for('index'))


@app.route('/admin/produto/criar', methods=['POST'])
@admin_required
def criar_produto():
    """Cria novo produto"""
    try:
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        estoque = int(request.form.get('estoque'))
        categoria = request.form.get('categoria')
        
        # Converte preço para centavos
        preco_centavos = round(preco * 100)
        
        produto = Product(
            nome=nome,
            descricao=descricao,
            preco=preco_centavos,
            estoque=estoque,
            categoria=categoria,
            ativo=True
        )
        
        produto.salvar()
        flash('Produto criado com sucesso!', 'success')
    
    except Exception as e:
        print(f"❌ Erro ao criar produto: {e}")
        flash('Erro ao criar produto', 'error')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/produto/deletar/<int:product_id>', methods=['POST'])
@admin_required
def deletar_produto(product_id):
    """Deleta produto (soft delete)"""
    try:
        produto = Product.buscar_por_id(product_id)
        if produto:
            produto.deletar()
            flash('Produto removido com sucesso!', 'success')
        else:
            flash('Produto não encontrado', 'error')
    
    except Exception as e:
        print(f"❌ Erro ao deletar produto: {e}")
        flash('Erro ao deletar produto', 'error')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/pedido/atualizar-status/<int:order_id>', methods=['POST'])
@admin_required
def atualizar_status_pedido(order_id):
    """Atualiza status do pedido"""
    try:
        novo_status = request.form.get('status')
        pedido = Order.buscar_por_id(order_id)
        
        if pedido:
            pedido.atualizar_status(novo_status)
            flash('Status atualizado com sucesso!', 'success')
        else:
            flash('Pedido não encontrado', 'error')
    
    except Exception as e:
        print(f"❌ Erro ao atualizar status: {e}")
        flash('Erro ao atualizar status', 'error')
    
    return redirect(url_for('admin_dashboard'))


# ==================== FILTRO JINJA2 ====================

@app.template_filter('preco')
def preco_filter(centavos):
    """Filtro para formatar preço"""
    return formatar_preco(centavos)


# ==================== EXECUÇÃO ====================

if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Pedidos - POO II")
    print("📍 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
