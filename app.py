from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime, date
import json
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sistema_doces_2024_seguro'

# Arquivos de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

PRODUTOS_FILE = os.path.join(DATA_DIR, 'produtos.json')
VENDAS_FILE = os.path.join(DATA_DIR, 'vendas.json')
FIADO_FILE = os.path.join(DATA_DIR, 'fiado.json')

# Credenciais admin (em produção, use hash!)
ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_data_atual_br():
    return datetime.now().strftime('%d/%m/%Y')

def get_data_atual_iso():
    return datetime.now().strftime('%Y-%m-%d')

# ==================== ROTAS ====================

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('vendas'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('vendas'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/vendas')
@login_required
def vendas():
    produtos = load_data(PRODUTOS_FILE)
    data_atual = get_data_atual_br()
    data_iso = get_data_atual_iso()
    return render_template('vendas.html', produtos=produtos, data_atual=data_atual, data_iso=data_iso)

@app.route('/api/vendas', methods=['POST'])
@login_required
def api_vendas():
    data = request.get_json()
    vendas = load_data(VENDAS_FILE)

    venda = {
        'id': len(vendas) + 1,
        'produto_id': data.get('produto_id'),
        'produto_nome': data.get('produto_nome'),
        'cliente': data.get('cliente'),
        'valor': float(data.get('valor', 0)),
        'quantidade': int(data.get('quantidade', 1)),
        'data': data.get('data'),
        'data_iso': data.get('data_iso'),
        'total': float(data.get('valor', 0)) * int(data.get('quantidade', 1)),
        'tipo': 'venda'
    }
    vendas.append(venda)
    save_data(VENDAS_FILE, vendas)
    return jsonify({'success': True, 'venda': venda})

@app.route('/produtos')
@login_required
def produtos():
    produtos = load_data(PRODUTOS_FILE)
    return render_template('produtos.html', produtos=produtos)

@app.route('/api/produtos', methods=['POST'])
@login_required
def api_produtos():
    data = request.get_json()
    produtos = load_data(PRODUTOS_FILE)

    produto = {
        'id': len(produtos) + 1,
        'nome': data.get('nome'),
        'preco': float(data.get('preco', 0)),
        'categoria': data.get('categoria', ''),
        'ativo': True
    }
    produtos.append(produto)
    save_data(PRODUTOS_FILE, produtos)
    return jsonify({'success': True, 'produto': produto})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
@login_required
def delete_produto(id):
    produtos = load_data(PRODUTOS_FILE)
    produtos = [p for p in produtos if p['id'] != id]
    save_data(PRODUTOS_FILE, produtos)
    return jsonify({'success': True})

@app.route('/relatorios')
@login_required
def relatorios():
    data_atual = get_data_atual_br()
    data_iso = get_data_atual_iso()
    return render_template('relatorios.html', data_atual=data_atual, data_iso=data_iso)

@app.route('/api/relatorios/<data>')
@login_required
def api_relatorios(data):
    vendas = load_data(VENDAS_FILE)

    # Filtrar por data
    vendas_dia = [v for v in vendas if v.get('data_iso') == data]

    # Agrupar por cliente
    clientes = {}
    for v in vendas_dia:
        cliente = v['cliente']
        if cliente not in clientes:
            clientes[cliente] = {'total': 0, 'quantidade': 0}
        clientes[cliente]['total'] += v['total']
        clientes[cliente]['quantidade'] += v['quantidade']

    # Ordenar por valor gasto (maior primeiro)
    clientes_ordenados = sorted(clientes.items(), key=lambda x: x[1]['total'], reverse=True)

    total_dia = sum(v['total'] for v in vendas_dia)

    return jsonify({
        'clientes': [{'nome': c[0], **c[1]} for c in clientes_ordenados],
        'total_dia': total_dia,
        'quantidade_vendas': len(vendas_dia)
    })

@app.route('/api/relatorios/ano/<ano>')
@login_required
def api_relatorios_ano(ano):
    vendas = load_data(VENDAS_FILE)

    # Filtrar por ano
    vendas_ano = [v for v in vendas if v.get('data_iso', '').startswith(ano)]

    # Agrupar por cliente
    clientes = {}
    for v in vendas_ano:
        cliente = v['cliente']
        if cliente not in clientes:
            clientes[cliente] = {'total': 0, 'quantidade': 0}
        clientes[cliente]['total'] += v['total']
        clientes[cliente]['quantidade'] += v['quantidade']

    # Ordenar por valor gasto
    clientes_ordenados = sorted(clientes.items(), key=lambda x: x[1]['total'], reverse=True)

    total_ano = sum(v['total'] for v in vendas_ano)

    return jsonify({
        'clientes': [{'nome': c[0], **c[1]} for c in clientes_ordenados],
        'total_ano': total_ano,
        'quantidade_vendas': len(vendas_ano)
    })

@app.route('/fiado')
@login_required
def fiado():
    fiados = load_data(FIADO_FILE)
    return render_template('fiado.html', fiados=fiados)

@app.route('/api/fiado', methods=['POST'])
@login_required
def api_fiado():
    data = request.get_json()
    fiados = load_data(FIADO_FILE)

    fiado = {
        'id': len(fiados) + 1,
        'cliente': data.get('cliente'),
        'produto': data.get('produto'),
        'valor': float(data.get('valor', 0)),
        'quantidade': int(data.get('quantidade', 1)),
        'total': float(data.get('valor', 0)) * int(data.get('quantidade', 1)),
        'data': data.get('data'),
        'data_iso': data.get('data_iso'),
        'pago': False,
        'data_pagamento': None
    }
    fiados.append(fiado)
    save_data(FIADO_FILE, fiados)
    return jsonify({'success': True, 'fiado': fiado})

@app.route('/api/fiado/<int:id>/pagar', methods=['POST'])
@login_required
def api_fiado_pagar(id):
    fiados = load_data(FIADO_FILE)
    for f in fiados:
        if f['id'] == id:
            f['pago'] = True
            f['data_pagamento'] = get_data_atual_br()
            break
    save_data(FIADO_FILE, fiados)
    return jsonify({'success': True})

@app.route('/api/fiado/<int:id>', methods=['DELETE'])
@login_required
def delete_fiado(id):
    fiados = load_data(FIADO_FILE)
    fiados = [f for f in fiados if f['id'] != id]
    save_data(FIADO_FILE, fiados)
    return jsonify({'success': True})

@app.route('/api/busca')
@login_required
def api_busca():
    termo = request.args.get('q', '').lower()
    tipo = request.args.get('tipo', 'todos')

    resultados = {'produtos': [], 'clientes': []}

    if tipo in ['todos', 'produtos']:
        produtos = load_data(PRODUTOS_FILE)
        resultados['produtos'] = [p for p in produtos if termo in p['nome'].lower()]

    if tipo in ['todos', 'clientes']:
        vendas = load_data(VENDAS_FILE)
        clientes = list(set(v['cliente'] for v in vendas if termo in v['cliente'].lower()))
        resultados['clientes'] = clientes

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
