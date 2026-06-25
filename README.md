# 🍬 Sistema de Controle de Vendas de Doces (com Banco de Dados SQLite)

Sistema mobile responsivo para controle de vendas de doces, desenvolvido com **Flask + SQLite**.

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

### Tabelas criadas automaticamente:
| Tabela | Descrição |
|--------|-----------|
| `produtos` | Produtos cadastrados |
| `vendas` | Registro de vendas |
| `fiados` | Contas fiado |

### Para ver os dados no banco (opcional):
```bash
# Instale o sqlite3 (se não tiver)
# No Windows: https://sqlite.org/download.html
# No Linux: sudo apt install sqlite3

# Acesse o banco
sqlite3 doces.db

# Veja as tabelas
.tables

# Veja as vendas
SELECT * FROM vendas;

# Veja total de vendas do dia
SELECT SUM(total) FROM vendas WHERE data_iso = date('now');

# Sair
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
├── app.py                 # Aplicação Flask + SQLite
├── requirements.txt       # Dependências (Flask, Flask-SQLAlchemy)
├── doces.db               # Banco de dados SQLite (criado auto)
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

## 💾 Backup do Banco

Para fazer backup, basta copiar o arquivo `doces.db`:
```bash
# Windows
copy doces.db doces_backup_2024.db

# Linux/Mac
cp doces.db doces_backup_2024.db
```
