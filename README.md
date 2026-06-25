# 🍬 Sistema de Controle de Vendas de Doces (com Banco de Dados SQLite)

Sistema mobile responsivo para controle de vendas de doces, desenvolvido com **Flask + SQLite**.

## 📋 Funcionalidades

- ✅ Login de Administrador
- 🛒 **Vendas**: Cadastro de vendas com produto, cliente, valor, data selecionável e quantidade
- 💳 **Fiado na tela Vendas**: Marque "Venda Fiado" e vai automaticamente para a tela Fiado
- 📦 **Produtos**: Cadastro simples de produtos com nome, preço e categoria
- 💳 **Fiado**: Controle de vendas fiado com pagamento e anotação manual
- 📊 **Relatórios**: 
  - Vendas do dia com ranking de clientes
  - Relatório anual com total e top clientes
  - Busca por data e cliente
- ➕ **Botão + no menu**: Acesso rápido para nova venda de qualquer tela

## 🚀 Como Executar

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Execute o sistema
```bash
python app.py
```

### 3. Acesse no navegador
```
http://localhost:5000
```

## 🔐 Login

- **Usuário:** `admin`
- **Senha:** `admin123`

## 🗄️ Banco de Dados SQLite

O sistema usa **SQLite** (banco de dados local, não precisa instalar nada extra). O arquivo `doces.db` é criado automaticamente na primeira execução.

### Tabelas:
| Tabela | Descrição |
|--------|-----------|
| `produtos` | Produtos cadastrados |
| `vendas` | Registro de todas as vendas (inclui fiado) |
| `fiados` | Contas fiado em aberto/pagas |

### Para ver os dados no banco:
```bash
sqlite3 doces.db
.tables
SELECT * FROM vendas;
SELECT * FROM fiados;
.quit
```

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
├── app.py                 # Flask + SQLite
├── requirements.txt       # Flask, Flask-SQLAlchemy
├── doces.db               # Banco SQLite (criado auto)
├── static/
│   ├── css/style.css      # Estilos responsivos
│   └── js/app.js          # JavaScript
└── templates/
    ├── base.html          # Menu com botão +
    ├── login.html         # Login
    ├── vendas.html        # Vendas + data selecionável + fiado
    ├── produtos.html      # Produtos
    ├── relatorios.html    # Relatórios
    └── fiado.html         # Fiado manual + fiado da venda
```
