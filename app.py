from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'sistema_doces_2024_seguro'

# Configuração do SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'doces.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== MODELOS ====================

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), default='')
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Venda(db.Model):
    __tablename__ = 'vendas'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    produto_nome = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    total = db.Column(db.Float, nullable=False)
    data = db.Column(db.String(10), nullable=False)
    data_iso = db.Column(db.String(10), nullable=False)
    is_fiado = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class Fiado(db.Model):
    __tablename__ = 'fiados'
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    produto = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    total = db.Column(db.Float, nullable=False)
    data = db.Column(db.String(10), nullable=False)
    data_iso = db.Column(db.String(10), nullable=False)
    pago = db.Column(db.Boolean, default=False)
    data_pagamento = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

# Criar tabelas
with app.app_context():
    db.create_all()

ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_data_atual_br():
    return datetime.now().strftime('%d/%m/%Y')

def get_data_atual_iso():
    return datetime.now().strftime('%Y-%m-%d')

def formatar_br(valor):
    """Converte float para formato BR: 5.0 -> '5,00'"""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Filtro Jinja para formatar moeda
@app.template_filter('moeda_br')
def moeda_br_filter(valor):
    return formatar_br(valor)

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
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    data_atual = get_data_atual_br()
    data_iso = get_data_atual_iso()
    return render_template('vendas.html', produtos=produtos, data_atual=data_atual, data_iso=data_iso)

@app.route('/api/vendas', methods=['POST'])
@login_required
def api_vendas():
    data = request.get_json()
    is_fiado = data.get('fiado', False)

    # Criar venda (sempre, fiado ou não)
    venda = Venda(
        produto_id=data.get('produto_id'),
        produto_nome=data.get('produto_nome'),
        cliente=data.get('cliente').strip(),
        valor=float(data.get('valor', 0)),
        quantidade=int(data.get('quantidade', 1)),
        total=float(data.get('valor', 0)) * int(data.get('quantidade', 1)),
        data=data.get('data'),
        data_iso=data.get('data_iso'),
        is_fiado=is_fiado
    )
    db.session.add(venda)
    db.session.flush()

    # Se for fiado, criar também na tabela fiado
    if is_fiado:
        fiado = Fiado(
            cliente=data.get('cliente').strip(),
            produto=data.get('produto_nome'),
            valor=float(data.get('valor', 0)),
            quantidade=int(data.get('quantidade', 1)),
            total=float(data.get('valor', 0)) * int(data.get('quantidade', 1)),
            data=data.get('data'),
            data_iso=data.get('data_iso'),
            pago=False
        )
        db.session.add(fiado)

    db.session.commit()

    return jsonify({'success': True, 'venda': {
        'id': venda.id,
        'produto_nome': venda.produto_nome,
        'cliente': venda.cliente,
        'total': venda.total,
        'quantidade': venda.quantidade,
        'fiado': is_fiado
    }})

@app.route('/produtos')
@login_required
def produtos():
    produtos = Produto.query.order_by(Produto.nome).all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/api/produtos', methods=['POST'])
@login_required
def api_produtos():
    data = request.get_json()

    produto = Produto(
        nome=data.get('nome').strip(),
        preco=float(data.get('preco', 0)),
        categoria=data.get('categoria', '').strip()
    )
    db.session.add(produto)
    db.session.commit()

    return jsonify({'success': True, 'produto': {
        'id': produto.id,
        'nome': produto.nome,
        'preco': produto.preco,
        'categoria': produto.categoria
    }})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
@login_required
def delete_produto(id):
    produto = Produto.query.get_or_404(id)
    produto.ativo = False
    db.session.commit()
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
    # TODAS as vendas do dia (inclui fiado) - fiado TAMBÉM é venda
    vendas = Venda.query.filter_by(data_iso=data).all()

    clientes_dict = {}
    for v in vendas:
        if v.cliente not in clientes_dict:
            clientes_dict[v.cliente] = {'total': 0, 'quantidade': 0}
        clientes_dict[v.cliente]['total'] += v.total
        clientes_dict[v.cliente]['quantidade'] += v.quantidade

    clientes_ordenados = sorted(clientes_dict.items(), key=lambda x: x[1]['total'], reverse=True)
    total_dia = sum(v.total for v in vendas)

    return jsonify({
        'clientes': [{'nome': c[0], **c[1]} for c in clientes_ordenados],
        'total_dia': total_dia,
        'quantidade_vendas': len(vendas)
    })

@app.route('/api/relatorios/ano/<ano>')
@login_required
def api_relatorios_ano(ano):
    # TODAS as vendas do ano (inclui fiado)
    vendas = Venda.query.filter(Venda.data_iso.like(f'{ano}-%')).all()

    clientes_dict = {}
    for v in vendas:
        if v.cliente not in clientes_dict:
            clientes_dict[v.cliente] = {'total': 0, 'quantidade': 0}
        clientes_dict[v.cliente]['total'] += v.total
        clientes_dict[v.cliente]['quantidade'] += v.quantidade

    clientes_ordenados = sorted(clientes_dict.items(), key=lambda x: x[1]['total'], reverse=True)
    total_ano = sum(v.total for v in vendas)

    return jsonify({
        'clientes': [{'nome': c[0], **c[1]} for c in clientes_ordenados],
        'total_ano': total_ano,
        'quantidade_vendas': len(vendas)
    })

@app.route('/fiado')
@login_required
def fiado():
    fiados = Fiado.query.order_by(Fiado.created_at.desc()).all()
    return render_template('fiado.html', fiados=fiados)

@app.route('/api/fiado', methods=['POST'])
@login_required
def api_fiado():
    data = request.get_json()

    fiado = Fiado(
        cliente=data.get('cliente').strip(),
        produto=data.get('produto').strip(),
        valor=float(data.get('valor', 0)),
        quantidade=int(data.get('quantidade', 1)),
        total=float(data.get('valor', 0)) * int(data.get('quantidade', 1)),
        data=data.get('data'),
        data_iso=data.get('data_iso')
    )
    db.session.add(fiado)
    db.session.commit()

    return jsonify({'success': True, 'fiado': {
        'id': fiado.id,
        'cliente': fiado.cliente,
        'total': fiado.total
    }})

@app.route('/api/fiado/<int:id>/pagar', methods=['POST'])
@login_required
def api_fiado_pagar(id):
    fiado = Fiado.query.get_or_404(id)
    fiado.pago = True
    fiado.data_pagamento = get_data_atual_br()
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/fiado/<int:id>', methods=['DELETE'])
@login_required
def delete_fiado(id):
    fiado = Fiado.query.get_or_404(id)
    db.session.delete(fiado)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/busca')
@login_required
def api_busca():
    termo = request.args.get('q', '').lower()
    tipo = request.args.get('tipo', 'todos')

    resultados = {'produtos': [], 'clientes': []}

    if tipo in ['todos', 'produtos']:
        produtos = Produto.query.filter(
            Produto.nome.ilike(f'%{termo}%'),
            Produto.ativo == True
        ).all()
        resultados['produtos'] = [{'id': p.id, 'nome': p.nome, 'preco': p.preco} for p in produtos]

    if tipo in ['todos', 'clientes']:
        clientes = db.session.query(Venda.cliente).filter(
            Venda.cliente.ilike(f'%{termo}%')
        ).distinct().all()
        resultados['clientes'] = [c[0] for c in clientes]

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
