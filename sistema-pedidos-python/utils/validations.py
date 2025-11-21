"""
Módulo de validações para o Sistema de Pedidos
Implementa validações usando regex e estruturas de decisão (if/else)
"""

import re


def validar_cpf(cpf):
    """
    Valida CPF usando regex e algoritmo de verificação de dígitos
    
    Args:
        cpf (str): CPF no formato 000.000.000-00 ou 00000000000
    
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_erro)
    """
    # Remove caracteres não numéricos
    cpf_limpo = re.sub(r'[^\d]', '', cpf)
    
    # Estrutura de decisão: verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        return False, 'CPF deve ter 11 dígitos'
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if re.match(r'^(\d)\1{10}$', cpf_limpo):
        return False, 'CPF inválido'
    
    # Validação do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf_limpo[i]) * (10 - i)
    
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0
    
    if resto != int(cpf_limpo[9]):
        return False, 'CPF inválido - dígito verificador incorreto'
    
    # Validação do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf_limpo[i]) * (11 - i)
    
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0
    
    if resto != int(cpf_limpo[10]):
        return False, 'CPF inválido - dígito verificador incorreto'
    
    return True, ''


def validar_email(email):
    """
    Valida email usando regex
    
    Args:
        email (str): Email a ser validado
    
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_erro)
    """
    # Estrutura de decisão: verifica se email está vazio
    if not email or email.strip() == '':
        return False, 'Email é obrigatório'
    
    # Regex para validação de email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(regex, email):
        return False, 'Email inválido'
    
    return True, ''


def validar_telefone(telefone):
    """
    Valida telefone brasileiro usando regex
    
    Args:
        telefone (str): Telefone no formato (00) 00000-0000 ou similar
    
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_erro)
    """
    # Estrutura de decisão: verifica se telefone está vazio
    if not telefone or telefone.strip() == '':
        return False, 'Telefone é obrigatório'
    
    # Regex para telefone brasileiro (com ou sem formatação)
    regex = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
    
    if not re.match(regex, telefone):
        return False, 'Telefone inválido. Use o formato (00) 00000-0000'
    
    return True, ''


def validar_idade(idade):
    """
    Valida idade mínima
    
    Args:
        idade (int): Idade a ser validada
    
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_erro)
    """
    try:
        idade_int = int(idade)
    except (ValueError, TypeError):
        return False, 'Idade deve ser um número'
    
    # Estrutura de decisão: valida idade mínima
    if idade_int < 18:
        return False, 'Idade mínima de 18 anos'
    
    if idade_int > 150:
        return False, 'Idade inválida'
    
    return True, ''


def validar_nome(nome):
    """
    Valida nome usando regex
    
    Args:
        nome (str): Nome a ser validado
    
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_erro)
    """
    # Estrutura de decisão: verifica se nome está vazio
    if not nome or nome.strip() == '':
        return False, 'Nome é obrigatório'
    
    if len(nome.strip()) < 3:
        return False, 'Nome deve ter pelo menos 3 caracteres'
    
    # Verifica se contém apenas letras e espaços
    regex = r'^[a-zA-ZÀ-ÿ\s]+$'
    if not re.match(regex, nome):
        return False, 'Nome deve conter apenas letras'
    
    return True, ''


def validar_endereco(endereco):
    """
    Valida endereço
    
    Args:
        endereco (str): Endereço a ser validado
    
    Returns:
        tuple: (bool, str) - (é_válido, mensagem_erro)
    """
    # Estrutura de decisão: verifica se endereço está vazio
    if not endereco or endereco.strip() == '':
        return False, 'Endereço é obrigatório'
    
    if len(endereco.strip()) < 10:
        return False, 'Endereço deve ter pelo menos 10 caracteres'
    
    return True, ''


def formatar_cpf(cpf):
    """
    Formata CPF para o padrão 000.000.000-00
    
    Args:
        cpf (str): CPF sem formatação
    
    Returns:
        str: CPF formatado
    """
    cpf_limpo = re.sub(r'[^\d]', '', cpf)
    if len(cpf_limpo) != 11:
        return cpf
    return f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'


def formatar_telefone(telefone):
    """
    Formata telefone para o padrão (00) 00000-0000
    
    Args:
        telefone (str): Telefone sem formatação
    
    Returns:
        str: Telefone formatado
    """
    tel_limpo = re.sub(r'[^\d]', '', telefone)
    
    if len(tel_limpo) == 11:
        return f'({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}'
    elif len(tel_limpo) == 10:
        return f'({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}'
    
    return telefone


def formatar_preco(centavos):
    """
    Formata preço de centavos para reais
    
    Args:
        centavos (int): Valor em centavos
    
    Returns:
        str: String formatada em reais
    """
    reais = centavos / 100
    return f'R$ {reais:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def converter_para_centavos(reais):
    """
    Converte preço em reais para centavos
    
    Args:
        reais (float): Valor em reais
    
    Returns:
        int: Valor em centavos
    """
    return round(float(reais) * 100)
