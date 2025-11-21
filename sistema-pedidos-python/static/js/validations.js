/**
 * Módulo de Validações Front-end
 * Implementa validações usando regex e estruturas de decisão (if/else)
 */

// ==================== VALIDAÇÃO DE CPF ====================

/**
 * Valida CPF usando regex e algoritmo de dígitos verificadores
 * @param {string} cpf - CPF a ser validado
 * @returns {object} - {isValid: boolean, error: string}
 */
function validarCPF(cpf) {
    // Remove caracteres não numéricos
    const cpfLimpo = cpf.replace(/[^\d]/g, '');
    
    // Estrutura de decisão: verifica se tem 11 dígitos
    if (cpfLimpo.length !== 11) {
        return { isValid: false, error: 'CPF deve ter 11 dígitos' };
    }
    
    // Regex para detectar CPFs com todos os dígitos iguais
    if (/^(\d)\1{10}$/.test(cpfLimpo)) {
        return { isValid: false, error: 'CPF inválido' };
    }
    
    // Validação do primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpfLimpo.charAt(i)) * (10 - i);
    }
    let resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpfLimpo.charAt(9))) {
        return { isValid: false, error: 'CPF inválido - dígito verificador incorreto' };
    }
    
    // Validação do segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpfLimpo.charAt(i)) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpfLimpo.charAt(10))) {
        return { isValid: false, error: 'CPF inválido - dígito verificador incorreto' };
    }
    
    return { isValid: true, error: '' };
}

// ==================== VALIDAÇÃO DE EMAIL ====================

/**
 * Valida email usando regex
 * @param {string} email - Email a ser validado
 * @returns {object} - {isValid: boolean, error: string}
 */
function validarEmail(email) {
    // Estrutura de decisão: verifica se email está vazio
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

// ==================== VALIDAÇÃO DE TELEFONE ====================

/**
 * Valida telefone brasileiro usando regex
 * @param {string} telefone - Telefone a ser validado
 * @returns {object} - {isValid: boolean, error: string}
 */
function validarTelefone(telefone) {
    // Estrutura de decisão: verifica se telefone está vazio
    if (!telefone || telefone.trim() === '') {
        return { isValid: false, error: 'Telefone é obrigatório' };
    }
    
    // Regex para telefone brasileiro (com ou sem formatação)
    const regex = /^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$/;
    
    if (!regex.test(telefone)) {
        return { isValid: false, error: 'Telefone inválido. Use o formato (00) 00000-0000' };
    }
    
    return { isValid: true, error: '' };
}

// ==================== VALIDAÇÃO DE IDADE ====================

/**
 * Valida idade mínima
 * @param {number} idade - Idade a ser validada
 * @returns {object} - {isValid: boolean, error: string}
 */
function validarIdade(idade) {
    // Estrutura de decisão: verifica se idade é um número
    if (!idade || isNaN(idade)) {
        return { isValid: false, error: 'Idade é obrigatória' };
    }
    
    const idadeNum = parseInt(idade);
    
    // Estrutura de decisão: valida idade mínima
    if (idadeNum < 18) {
        return { isValid: false, error: 'Idade mínima de 18 anos' };
    }
    
    if (idadeNum > 150) {
        return { isValid: false, error: 'Idade inválida' };
    }
    
    return { isValid: true, error: '' };
}

// ==================== VALIDAÇÃO DE NOME ====================

/**
 * Valida nome usando regex
 * @param {string} nome - Nome a ser validado
 * @returns {object} - {isValid: boolean, error: string}
 */
function validarNome(nome) {
    // Estrutura de decisão: verifica se nome está vazio
    if (!nome || nome.trim() === '') {
        return { isValid: false, error: 'Nome é obrigatório' };
    }
    
    if (nome.trim().length < 3) {
        return { isValid: false, error: 'Nome deve ter pelo menos 3 caracteres' };
    }
    
    // Regex para verificar se contém apenas letras e espaços
    const regex = /^[a-zA-ZÀ-ÿ\s]+$/;
    if (!regex.test(nome)) {
        return { isValid: false, error: 'Nome deve conter apenas letras' };
    }
    
    return { isValid: true, error: '' };
}

// ==================== VALIDAÇÃO DE ENDEREÇO ====================

/**
 * Valida endereço
 * @param {string} endereco - Endereço a ser validado
 * @returns {object} - {isValid: boolean, error: string}
 */
function validarEndereco(endereco) {
    // Estrutura de decisão: verifica se endereço está vazio
    if (!endereco || endereco.trim() === '') {
        return { isValid: false, error: 'Endereço é obrigatório' };
    }
    
    if (endereco.trim().length < 10) {
        return { isValid: false, error: 'Endereço deve ter pelo menos 10 caracteres' };
    }
    
    return { isValid: true, error: '' };
}

// ==================== VALIDAÇÃO DE SENHA ====================

/**
 * Valida senha
 * @param {string} senha - Senha a ser validada
 * @returns {object} - {isValid: boolean, error: string}
 */
function validarSenha(senha) {
    // Estrutura de decisão: verifica se senha está vazia
    if (!senha || senha.trim() === '') {
        return { isValid: false, error: 'Senha é obrigatória' };
    }
    
    if (senha.length < 6) {
        return { isValid: false, error: 'Senha deve ter pelo menos 6 caracteres' };
    }
    
    return { isValid: true, error: '' };
}

// ==================== FORMATAÇÃO ====================

/**
 * Formata CPF para o padrão 000.000.000-00
 * @param {string} cpf - CPF sem formatação
 * @returns {string} - CPF formatado
 */
function formatarCPF(cpf) {
    const cpfLimpo = cpf.replace(/[^\d]/g, '');
    if (cpfLimpo.length !== 11) return cpf;
    return cpfLimpo.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
}

/**
 * Formata telefone para o padrão (00) 00000-0000
 * @param {string} telefone - Telefone sem formatação
 * @returns {string} - Telefone formatado
 */
function formatarTelefone(telefone) {
    const telLimpo = telefone.replace(/[^\d]/g, '');
    
    if (telLimpo.length === 11) {
        return telLimpo.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (telLimpo.length === 10) {
        return telLimpo.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    }
    
    return telefone;
}

// ==================== EXIBIÇÃO DE ERROS ====================

/**
 * Exibe mensagem de erro em um campo
 * @param {string} fieldId - ID do campo
 * @param {string} message - Mensagem de erro
 */
function mostrarErro(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    // Adiciona classe de erro ao campo
    field.classList.add('error');
    
    // Remove erro anterior se existir
    const errorExistente = field.parentElement.querySelector('.form-error');
    if (errorExistente) {
        errorExistente.remove();
    }
    
    // Cria e adiciona nova mensagem de erro
    if (message) {
        const errorSpan = document.createElement('span');
        errorSpan.className = 'form-error';
        errorSpan.textContent = message;
        field.parentElement.appendChild(errorSpan);
    }
}

/**
 * Remove mensagem de erro de um campo
 * @param {string} fieldId - ID do campo
 */
function limparErro(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    // Remove classe de erro
    field.classList.remove('error');
    
    // Remove mensagem de erro
    const errorSpan = field.parentElement.querySelector('.form-error');
    if (errorSpan) {
        errorSpan.remove();
    }
}

/**
 * Valida campo individual
 * @param {string} fieldId - ID do campo
 * @param {string} fieldName - Nome do campo para validação
 * @returns {boolean} - True se válido
 */
function validarCampo(fieldId, fieldName) {
    const field = document.getElementById(fieldId);
    if (!field) return false;
    
    const value = field.value;
    let resultado;
    
    // Estrutura de decisão: escolhe validação baseada no nome do campo
    switch(fieldName) {
        case 'nome':
            resultado = validarNome(value);
            break;
        case 'email':
            resultado = validarEmail(value);
            break;
        case 'cpf':
            resultado = validarCPF(value);
            break;
        case 'telefone':
            resultado = validarTelefone(value);
            break;
        case 'idade':
            resultado = validarIdade(value);
            break;
        case 'endereco':
            resultado = validarEndereco(value);
            break;
        case 'senha':
            resultado = validarSenha(value);
            break;
        default:
            return true;
    }
    
    if (resultado.isValid) {
        limparErro(fieldId);
        return true;
    } else {
        mostrarErro(fieldId, resultado.error);
        return false;
    }
}
