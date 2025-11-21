"""
Script para popular banco de dados com produtos de exemplo
"""

from models.product import Product
from models.user import User

print("🌱 Iniciando seed do banco de dados...")

# Produtos de exemplo
produtos = [
    {
        'nome': 'Notebook Dell Inspiron 15',
        'descricao': 'Notebook com processador Intel Core i5, 8GB RAM, SSD 256GB',
        'preco': 299900,  # R$ 2.999,00
        'estoque': 15,
        'categoria': 'Eletrônicos',
        'ativo': True
    },
    {
        'nome': 'Mouse Logitech MX Master 3',
        'descricao': 'Mouse ergonômico sem fio com sensor de alta precisão',
        'preco': 45900,  # R$ 459,00
        'estoque': 30,
        'categoria': 'Periféricos',
        'ativo': True
    },
    {
        'nome': 'Teclado Mecânico Keychron K2',
        'descricao': 'Teclado mecânico sem fio com switches Gateron Brown',
        'preco': 59900,  # R$ 599,00
        'estoque': 20,
        'categoria': 'Periféricos',
        'ativo': True
    },
    {
        'nome': 'Monitor LG 27" 4K',
        'descricao': 'Monitor IPS 27 polegadas com resolução 4K UHD',
        'preco': 189900,  # R$ 1.899,00
        'estoque': 10,
        'categoria': 'Monitores',
        'ativo': True
    },
    {
        'nome': 'Webcam Logitech C920',
        'descricao': 'Webcam Full HD 1080p com microfone embutido',
        'preco': 39900,  # R$ 399,00
        'estoque': 25,
        'categoria': 'Periféricos',
        'ativo': True
    },
    {
        'nome': 'Headset HyperX Cloud II',
        'descricao': 'Headset gamer com som surround 7.1 virtual',
        'preco': 49900,  # R$ 499,00
        'estoque': 18,
        'categoria': 'Áudio',
        'ativo': True
    },
    {
        'nome': 'SSD Samsung 1TB',
        'descricao': 'SSD NVMe M.2 1TB com velocidade de leitura de 3500MB/s',
        'preco': 69900,  # R$ 699,00
        'estoque': 35,
        'categoria': 'Armazenamento',
        'ativo': True
    },
    {
        'nome': 'Cadeira Gamer DXRacer',
        'descricao': 'Cadeira ergonômica para gamers com ajuste de altura e inclinação',
        'preco': 129900,  # R$ 1.299,00
        'estoque': 8,
        'categoria': 'Móveis',
        'ativo': True
    },
    {
        'nome': 'Mousepad Gamer Grande',
        'descricao': 'Mousepad de tecido 90x40cm com base antiderrapante',
        'preco': 8900,  # R$ 89,00
        'estoque': 50,
        'categoria': 'Acessórios',
        'ativo': True
    },
    {
        'nome': 'Hub USB-C 7 em 1',
        'descricao': 'Hub com HDMI, USB 3.0, leitor de cartão SD e carregamento PD',
        'preco': 15900,  # R$ 159,00
        'estoque': 40,
        'categoria': 'Acessórios',
        'ativo': True
    }
]

try:
    for produto_data in produtos:
        produto = Product(**produto_data)
        produto.salvar()
        print(f"✅ Produto criado: {produto.nome}")
    
    print(f"\n🎉 Seed concluído! {len(produtos)} produtos adicionados ao banco.")
    
    # Cria usuário admin de exemplo
    print("\n👤 Criando usuário administrador de exemplo...")
    admin = User(
        nome='Administrador Sistema',
        email='admin@sistema.com',
        senha='admin123',
        cpf='12345678901',
        telefone='11987654321',
        idade=25,
        endereco='Rua Exemplo, 123 - São Paulo - SP',
        role='admin'
    )
    admin.salvar()
    print("✅ Admin criado: admin@sistema.com / senha: admin123")

except Exception as e:
    print(f"❌ Erro ao executar seed: {e}")
