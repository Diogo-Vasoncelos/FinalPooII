# 🚀 Instruções Rápidas de Instalação

## Pré-requisitos

- Python 3.11 ou superior
- MySQL 8.x ou superior
- pip (gerenciador de pacotes Python)

## Passo a Passo

### 1. Extrair o ZIP

Extraia o arquivo `sistema-pedidos-python.zip` em uma pasta de sua preferência.

### 2. Criar Ambiente Virtual

```bash
cd sistema-pedidos-python
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados MySQL

#### Opção A: Via MySQL Workbench
1. Abra o MySQL Workbench
2. Conecte ao servidor MySQL
3. Abra o arquivo `schema.sql`
4. Execute o script

#### Opção B: Via Linha de Comando
```bash
mysql -u root -p < schema.sql
```

### 5. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=sistema_pedidos
SECRET_KEY=chave-secreta-qualquer
```

### 6. Popular Banco com Dados de Teste

```bash
python seed.py
```

Este comando adiciona:
- ✅ 10 produtos de exemplo
- ✅ 1 usuário administrador

### 7. Executar a Aplicação

```bash
python app.py
```

O sistema estará disponível em: **http://localhost:5000**

### 8. Acessar o Sistema

#### Conta Administrador (pré-criada)
- **Email:** admin@sistema.com
- **Senha:** admin123

#### Criar Nova Conta
1. Clique em "Cadastrar"
2. Preencha todos os campos
3. Use um CPF válido (ex: 123.456.789-09)
4. Telefone: (11) 98765-4321
5. Idade mínima: 18 anos

---

## ⚠️ Problemas Comuns

### Erro: "No module named 'flask'"
**Solução:** Ative o ambiente virtual e instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Access denied for user"
**Solução:** Verifique as credenciais no arquivo `.env`

### Erro: "Unknown database 'sistema_pedidos'"
**Solução:** Execute o script `schema.sql` no MySQL

### Porta 5000 já está em uso
**Solução:** Edite `app.py` e altere a porta:
```python
app.run(debug=True, port=5001)
```

---

## 📚 Documentação Completa

Para mais detalhes, consulte o arquivo **README.md** completo.

---

## 🎓 Projeto Acadêmico

Este sistema foi desenvolvido para a disciplina de **POO II** da Faculdade Anhanguera.

**Tecnologias:** Python + Flask + HTML5 + CSS3 + JavaScript + MySQL
