# Sistema de Pedidos Online - POO II

**Projeto Acadêmico de Programação Orientada a Objetos II**

Sistema web completo de gerenciamento de pedidos desenvolvido com **Python/Flask + HTML5 + CSS3 + JavaScript**, implementando validações robustas, autenticação segura e controle de acesso por roles.

---

## 📋 Sumário

1. [Visão Geral](#visão-geral)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Validações Implementadas](#validações-implementadas)
5. [Fluxo de Autenticação](#fluxo-de-autenticação)
6. [Instalação e Execução](#instalação-e-execução)
7. [Estrutura do Projeto](#estrutura-do-projeto)
8. [Funcionalidades](#funcionalidades)
9. [Considerações de Segurança](#considerações-de-segurança)

---

## 🎯 Visão Geral

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de **Programação Orientada a Objetos II (POO II)** da Faculdade Anhanguera, atendendo todos os requisitos especificados no documento oficial.

O sistema permite que clientes realizem pedidos de produtos de forma segura e intuitiva, enquanto administradores gerenciam o catálogo de produtos, acompanham pedidos e visualizam informações dos clientes.

### Objetivos do Projeto

- Implementar validações usando **expressões regulares (regex)** para CPF, email e telefone
- Aplicar **estruturas de decisão (if/else, switch)** no processo de validação
- Utilizar **try/except** para tratamento robusto de exceções
- Desenvolver sistema de autenticação com **controle de sessões**
- Implementar **controle de acesso baseado em roles** (cliente/administrador)
- Criar interface responsiva seguindo princípios de UX
- Garantir segurança contra vulnerabilidades comuns

---

## 🛠 Tecnologias Utilizadas

### Back-end

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Python** | 3.11+ | Linguagem de programação principal |
| **Flask** | 3.0.0 | Framework web minimalista |
| **Flask-Session** | 0.5.0 | Gerenciamento de sessões |
| **Werkzeug** | 3.0.1 | Utilitários WSGI (hash de senhas) |
| **mysql-connector-python** | 8.2.0 | Conector MySQL para Python |
| **python-dotenv** | 1.0.0 | Gerenciamento de variáveis de ambiente |

### Front-end

| Tecnologia | Descrição |
|------------|-----------|
| **HTML5** | Estrutura semântica das páginas |
| **CSS3** | Estilização responsiva com variáveis CSS |
| **JavaScript** | Validações client-side e interatividade |

### Banco de Dados

| Tecnologia | Descrição |
|------------|-----------|
| **MySQL** | Sistema de gerenciamento de banco de dados relacional |

---

## 🏗 Arquitetura do Sistema

O sistema segue uma arquitetura **MVC (Model-View-Controller)** adaptada para Flask:

```
sistema-pedidos-python/
├── app.py                  # Aplicação Flask principal (Controller)
├── models/                 # Models (POO)
│   ├── user.py            # Classe User
│   ├── product.py         # Classe Product
│   └── order.py           # Classes Order e OrderItem
├── templates/             # Views (HTML)
│   ├── base.html          # Template base
│   ├── index.html         # Landing page
│   ├── login.html         # Página de login
│   ├── cadastro.html      # Página de cadastro
│   ├── cliente_dashboard.html
│   └── admin_dashboard.html
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── styles.css     # CSS global
│   └── js/
│       └── validations.js # Validações JavaScript
├── utils/                 # Utilitários
│   ├── database.py        # Conexão com banco
│   └── validations.py     # Validações Python
├── schema.sql             # Schema do banco de dados
├── seed.py                # Script para popular banco
├── requirements.txt       # Dependências Python
└── .env.example           # Exemplo de variáveis de ambiente
```

### Fluxo de Dados

1. **Cliente** → Acessa página HTML
2. **JavaScript** → Valida dados no front-end (regex, if/else)
3. **Formulário** → Envia dados para rota Flask
4. **Flask** → Valida novamente no back-end (try/except)
5. **Model** → Interage com banco de dados MySQL
6. **Resposta** → Retorna para o template HTML

---

## ✅ Validações Implementadas

O sistema implementa validações em **duas camadas** (front-end e back-end) conforme requisitos do projeto.

### Validações Front-end (JavaScript)

Implementadas em `static/js/validations.js` usando **regex** e **estruturas de decisão**:

#### 1. Validação de CPF

```javascript
function validarCPF(cpf) {
    const cpfLimpo = cpf.replace(/[^\d]/g, '');
    
    // Estrutura de decisão: verifica se tem 11 dígitos
    if (cpfLimpo.length !== 11) {
        return { isValid: false, error: 'CPF deve ter 11 dígitos' };
    }
    
    // Regex para detectar CPFs com todos os dígitos iguais
    if (/^(\d)\1{10}$/.test(cpfLimpo)) {
        return { isValid: false, error: 'CPF inválido' };
    }
    
    // Validação dos dígitos verificadores...
    return { isValid: true, error: '' };
}
```

**Regex utilizado:** `/^(\d)\1{10}$/` - Detecta CPFs com todos os dígitos iguais

#### 2. Validação de Email

```javascript
function validarEmail(email) {
    // Estrutura de decisão
    if (!email || email.trim() === '') {
        return { isValid: false, error: 'Email é obrigatório' };
    }
    
    // Regex para validação de email
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    if (!regex.test(email)) {
        return { isValid: false, error: 'Email inválido' };
    }
    
    return { isValid: true, error: '' };
}
```

**Regex utilizado:** `/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/`

#### 3. Validação de Telefone

```javascript
function validarTelefone(telefone) {
    // Estrutura de decisão
    if (!telefone || telefone.trim() === '') {
        return { isValid: false, error: 'Telefone é obrigatório' };
    }
    
    // Regex para telefone brasileiro
    const regex = /^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$/;
    
    if (!regex.test(telefone)) {
        return { isValid: false, error: 'Telefone inválido' };
    }
    
    return { isValid: true, error: '' };
}
```

**Regex utilizado:** `/^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$/`

### Validações Back-end (Python)

Implementadas em `utils/validations.py` e `models/user.py` usando **regex**, **if/else** e **try/except**:

#### 1. Validação de CPF com Algoritmo

```python
def validar_cpf(cpf):
    """Valida CPF usando regex e algoritmo de verificação"""
    cpf_limpo = re.sub(r'[^\d]', '', cpf)
    
    # Estrutura de decisão
    if len(cpf_limpo) != 11:
        return False, 'CPF deve ter 11 dígitos'
    
    # Regex para detectar CPFs inválidos
    if re.match(r'^(\d)\1{10}$', cpf_limpo):
        return False, 'CPF inválido'
    
    # Validação dos dígitos verificadores...
    return True, ''
```

#### 2. Tratamento de Exceções

```python
def salvar(self):
    """Salva usuário no banco de dados"""
    # Try/Except para tratamento de exceções
    try:
        # Valida dados antes de salvar
        valido, erros = self.validar()
        if not valido:
            raise ValueError(f"Dados inválidos: {erros}")
        
        # Verifica unicidade de email
        if self.email_existe():
            raise ValueError("Email já cadastrado")
        
        # Insere no banco...
        
    except Exception as e:
        print(f"❌ Erro ao salvar usuário: {e}")
        raise e
```

### Tabela Resumo das Validações

| Campo | Front-end | Back-end | Regex | Algoritmo |
|-------|-----------|----------|-------|-----------|
| **Nome** | Min 3 caracteres, apenas letras | Min 3 caracteres | `/^[a-zA-ZÀ-ÿ\s]+$/` | - |
| **Email** | Formato válido | Formato válido + unicidade | `/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/` | - |
| **CPF** | 11 dígitos + dígitos verificadores | Algoritmo completo + unicidade | `/^(\d)\1{10}$/` | Sim |
| **Telefone** | Formato brasileiro | Formato brasileiro | `/^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$/` | - |
| **Idade** | Min 18, max 150 | Min 18 | - | - |
| **Endereço** | Min 10 caracteres | Min 10 caracteres | - | - |
| **Senha** | Min 6 caracteres | Min 6 + hash seguro | - | - |

---

## 🔐 Fluxo de Autenticação

O sistema implementa autenticação segura com controle de sessões usando **Flask-Session**.

### Diagrama de Fluxo

```
1. Usuário acessa /login
2. Preenche email e senha
3. Flask valida credenciais
4. Verifica senha hasheada (Werkzeug)
5. Cria sessão com session['user_id']
6. Redireciona para dashboard apropriado
7. Decorators verificam sessão em cada requisição
```

### Decorators de Controle de Acesso

#### 1. Login Required

```python
def login_required(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

#### 2. Admin Required

```python
def admin_required(f):
    """Decorator para rotas que requerem permissão de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.buscar_por_id(session['user_id'])
        if not user or user.role != 'admin':
            flash('Acesso negado', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- MySQL 8.x ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/sistema-pedidos-python.git
cd sistema-pedidos-python
```

### Passo 2: Criar Ambiente Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados

```bash
# Criar banco de dados MySQL
mysql -u root -p < schema.sql
```

### Passo 5: Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=sistema_pedidos
SECRET_KEY=sua-chave-secreta
```

### Passo 6: Popular Banco com Dados de Teste

```bash
python seed.py
```

Este comando adiciona:
- 10 produtos de exemplo
- 1 usuário administrador (admin@sistema.com / admin123)

### Passo 7: Executar Aplicação

```bash
python app.py
```

O sistema estará disponível em `http://localhost:5000`

### Passo 8: Acessar o Sistema

1. Abra o navegador em `http://localhost:5000`
2. Clique em "Cadastrar" para criar uma conta
3. Ou faça login com a conta admin: `admin@sistema.com` / `admin123`

---

## 📁 Estrutura do Projeto

```
sistema-pedidos-python/
│
├── app.py                      # Aplicação Flask principal
│   ├── Rotas públicas (/, /login, /cadastro)
│   ├── Rotas do cliente (/cliente/dashboard)
│   ├── Rotas do admin (/admin/*)
│   └── Decorators de autenticação
│
├── models/                     # Classes POO
│   ├── user.py                # Classe User
│   │   ├── validar()          # Validação de dados
│   │   ├── salvar()           # Inserir no banco
│   │   ├── atualizar()        # Atualizar registro
│   │   └── buscar_por_*()     # Queries
│   ├── product.py             # Classe Product
│   └── order.py               # Classes Order e OrderItem
│
├── utils/                      # Utilitários
│   ├── database.py            # Classe Database
│   │   ├── connect()          # Conexão MySQL
│   │   ├── execute_query()    # INSERT/UPDATE/DELETE
│   │   ├── fetch_one()        # SELECT único
│   │   └── fetch_all()        # SELECT múltiplo
│   └── validations.py         # Funções de validação
│       ├── validar_cpf()      # Valida CPF
│       ├── validar_email()    # Valida email
│       ├── validar_telefone() # Valida telefone
│       └── formatar_*()       # Formatação
│
├── templates/                  # Views HTML
│   ├── base.html              # Template base
│   ├── index.html             # Landing page
│   ├── login.html             # Login
│   ├── cadastro.html          # Cadastro com validações JS
│   ├── cliente_dashboard.html # Dashboard do cliente
│   └── admin_dashboard.html   # Dashboard admin com tabs
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   └── styles.css         # CSS global responsivo
│   └── js/
│       └── validations.js     # Validações JavaScript
│           ├── validarCPF()
│           ├── validarEmail()
│           ├── validarTelefone()
│           ├── formatarCPF()
│           └── mostrarErro()
│
├── schema.sql                  # Schema do banco de dados
├── seed.py                     # Script de seed
├── requirements.txt            # Dependências Python
├── .env.example                # Exemplo de variáveis
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

---

## 🎯 Funcionalidades

### Para Clientes

- ✅ Cadastro com validações completas (CPF, email, telefone, idade)
- ✅ Login seguro com senha hasheada
- ✅ Dashboard personalizado com estatísticas
- ✅ Visualização de pedidos realizados
- ✅ Histórico completo com status atualizado
- ✅ Visualização de dados pessoais

### Para Administradores

- ✅ Dashboard administrativo com métricas gerais
- ✅ Gerenciamento de produtos (CRUD completo)
- ✅ Criação de novos produtos via modal
- ✅ Remoção de produtos (soft delete)
- ✅ Visualização de todos os pedidos
- ✅ Atualização de status de pedidos
- ✅ Listagem de todos os clientes
- ✅ Interface com tabs para organização

### Validações

- ✅ Validações em tempo real no front-end
- ✅ Revalidação no back-end
- ✅ Mensagens de erro claras
- ✅ Formatação automática de CPF e telefone
- ✅ Verificação de unicidade (email e CPF)
- ✅ Tratamento de exceções robusto

---

## 🔒 Considerações de Segurança

### 1. Senhas Hasheadas

Todas as senhas são hasheadas usando **Werkzeug** (PBKDF2 + SHA256):

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Ao salvar
senha_hash = generate_password_hash(senha)

# Ao verificar
check_password_hash(senha_hash, senha_fornecida)
```

### 2. Proteção contra SQL Injection

Todas as queries usam **parâmetros** ao invés de concatenação:

```python
# ✅ Seguro
query = "SELECT * FROM users WHERE email = %s"
result = db.fetch_one(query, (email,))

# ❌ Inseguro (NÃO utilizado)
# query = f"SELECT * FROM users WHERE email = '{email}'"
```

### 3. Controle de Sessões

- Sessões armazenadas no servidor (Flask-Session)
- Timeout automático de sessão
- Verificação em cada requisição protegida

### 4. Validação em Múltiplas Camadas

- Front-end: Feedback imediato ao usuário
- Back-end: Segurança e consistência
- Banco de dados: Constraints e unicidade

### 5. Proteção contra XSS

- Templates Jinja2 escapam automaticamente HTML
- Validação de inputs no back-end

---

## 📊 Modelo de Dados

### Diagrama ER

```
┌─────────────┐         ┌──────────────┐
│    users    │         │   products   │
├─────────────┤         ├──────────────┤
│ id (PK)     │         │ id (PK)      │
│ nome        │         │ nome         │
│ email       │         │ descricao    │
│ senha       │         │ preco        │
│ cpf         │         │ estoque      │
│ telefone    │         │ ativo        │
│ idade       │         │ categoria    │
│ endereco    │         └──────────────┘
│ role        │                │
└─────────────┘                │
       │                       │
       │ 1:N                   │
       ▼                       │
┌─────────────┐                │
│   orders    │                │
├─────────────┤                │
│ id (PK)     │                │
│ user_id(FK) │◄───────────────┘
│ status      │         N:M
│ valor_total │
│ endereco    │         ┌──────────────┐
└─────────────┘         │ order_items  │
       │                ├──────────────┤
       │ 1:N            │ id (PK)      │
       └───────────────►│ order_id(FK) │
                        │ product_id   │
                        │ quantidade   │
                        │ preco_unit   │
                        └──────────────┘
```

---

## 📝 Relatório Técnico

### Contexto Comercial Escolhido

**Loja Virtual de Produtos de Tecnologia**

O sistema simula uma loja online especializada em produtos de tecnologia (notebooks, periféricos, monitores, etc.), permitindo que clientes visualizem seus pedidos e administradores gerenciem o catálogo e acompanhem vendas.

### Validações Implementadas

#### Front-end (JavaScript)

- **Estruturas de decisão:** if/else e switch para validação de campos
- **Expressões regulares:** Validação de CPF, email e telefone
- **Mensagens de erro:** Feedback imediato ao usuário
- **Formatação automática:** CPF e telefone formatados durante digitação

#### Back-end (Python)

- **Revalidação de dados:** Todos os dados são revalidados no servidor
- **Try/except:** Tratamento robusto de exceções em todas as operações
- **Expressões regulares:** Validação de formatos
- **Estruturas condicionais:** Verificação de regras de negócio
- **Validação de credenciais:** Verificação de senha hasheada
- **Gestão de sessões:** Controle de acesso restrito

### Estrutura do Banco de Dados

O banco foi modelado seguindo princípios de normalização (3FN):

- **users:** Armazena dados dos usuários com constraints de unicidade
- **products:** Catálogo de produtos com controle de estoque
- **orders:** Pedidos realizados pelos clientes
- **order_items:** Relacionamento N:N entre pedidos e produtos

### Fluxo de Autenticação

1. Usuário acessa página de login
2. Preenche credenciais (email + senha)
3. Flask valida credenciais no banco
4. Verifica senha hasheada com Werkzeug
5. Cria sessão com Flask-Session
6. Armazena user_id, user_name e user_role na sessão
7. Redireciona para dashboard apropriado baseado no role
8. Decorators verificam sessão em rotas protegidas
9. Logout limpa sessão do servidor

### Prints das Principais Telas

1. **Landing Page:** Apresentação do sistema com call-to-action
2. **Cadastro:** Formulário com validações em tempo real
3. **Login:** Autenticação simples e segura
4. **Dashboard Cliente:** Estatísticas e lista de pedidos
5. **Dashboard Admin:** Tabs para produtos, pedidos e clientes

### Boas Práticas e Segurança

- Senhas hasheadas com PBKDF2 + SHA256
- Queries parametrizadas (proteção SQL injection)
- Validações em múltiplas camadas
- Controle de sessões no servidor
- Separação de responsabilidades (MVC)
- Código comentado e organizado
- Tratamento de exceções robusto
- Constraints no banco de dados

---

## 👥 Autor

**Projeto Acadêmico - POO II**

Desenvolvido para a disciplina de Programação Orientada a Objetos II da Faculdade Anhanguera.

---

## 📄 Licença

Este projeto é de uso acadêmico e educacional.

---

**Desenvolvido com Python 🐍 + Flask 🌶️ + HTML5 + CSS3 + JavaScript**
