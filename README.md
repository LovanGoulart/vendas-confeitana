# 🍬 Sistema de Controle de Vendas de Doces

Sistema mobile responsivo para controle de vendas de doces, desenvolvido com Flask, HTML, CSS e JavaScript.

## 📋 Funcionalidades

- ✅ Login de Administrador
- 🛒 **Vendas**: Cadastro de vendas com produto, cliente, valor, data e quantidade
- 📦 **Produtos**: Cadastro simples de produtos com nome, preço e categoria
- 💳 **Fiado**: Controle de vendas fiado com pagamento
- 📊 **Relatórios**: 
  - Vendas do dia com ranking de clientes
  - Relatório anual com total e top clientes
  - Busca por data e cliente

## 🚀 Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o sistema:
```bash
python app.py
```

3. Acesse no navegador:
```
http://localhost:5000
```

## 🔐 Login

- **Usuário:** `admin`
- **Senha:** `admin123`

## 📱 Acesso Mobile

O sistema é totalmente responsivo. Para acessar pelo celular na mesma rede:

1. Descubra o IP do computador:
```bash
ipconfig  # Windows
ifconfig  # Linux/Mac
```

2. Acesse pelo celular:
```
http://IP_DO_COMPUTADOR:5000
```

## 📁 Estrutura

```
sistema_doces/
├── app.py                 # Aplicação Flask
├── requirements.txt       # Dependências
├── data/                  # Dados JSON (criado automaticamente)
│   ├── produtos.json
│   ├── vendas.json
│   └── fiado.json
├── static/
│   ├── css/style.css      # Estilos responsivos
│   └── js/app.js          # JavaScript
└── templates/
    ├── base.html          # Template base
    ├── login.html         # Tela de login
    ├── vendas.html        # Tela de vendas
    ├── produtos.html      # Tela de produtos
    ├── relatorios.html    # Tela de relatórios
    └── fiado.html         # Tela de fiado
```

## 💾 Dados

Todos os dados são salvos em arquivos JSON na pasta `data/`. Não é necessário banco de dados.
