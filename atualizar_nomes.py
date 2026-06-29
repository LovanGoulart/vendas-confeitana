#!/usr/bin/env python3
"""
Script para normalizar nomes de clientes no banco de dados.
Converte todos os nomes para minúsculas e mescla registros duplicados.
"""

import sqlite3
import os

# Caminho do banco (mesmo do app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'doces.db')

def normalizar_nomes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("🔧 Normalizando nomes de clientes...")
    print(f"📁 Banco: {DB_PATH}")
    print()

    # ========== TABELA VENDAS ==========
    print("📊 Tabela 'vendas':")

    # Ver nomes antes
    cursor.execute("SELECT DISTINCT cliente FROM vendas ORDER BY cliente")
    nomes_antes = cursor.fetchall()
    print(f"   Nomes únicos antes: {len(nomes_antes)}")
    for nome in nomes_antes:
        print(f"      - {nome[0]}")

    # Converter para minúsculas
    cursor.execute("UPDATE vendas SET cliente = LOWER(cliente)")
    vendas_atualizadas = cursor.rowcount
    print(f"   ✅ {vendas_atualizadas} registros atualizados")

    # Ver nomes depois
    cursor.execute("SELECT DISTINCT cliente FROM vendas ORDER BY cliente")
    nomes_depois = cursor.fetchall()
    print(f"   Nomes únicos depois: {len(nomes_depois)}")
    for nome in nomes_depois:
        print(f"      - {nome[0]}")
    print()

    # ========== TABELA FIADOS ==========
    print("📊 Tabela 'fiados':")

    # Ver nomes antes
    cursor.execute("SELECT DISTINCT cliente FROM fiados ORDER BY cliente")
    nomes_antes = cursor.fetchall()
    print(f"   Nomes únicos antes: {len(nomes_antes)}")
    for nome in nomes_antes:
        print(f"      - {nome[0]}")

    # Converter para minúsculas
    cursor.execute("UPDATE fiados SET cliente = LOWER(cliente)")
    fiados_atualizados = cursor.rowcount
    print(f"   ✅ {fiados_atualizados} registros atualizados")

    # Ver nomes depois
    cursor.execute("SELECT DISTINCT cliente FROM fiados ORDER BY cliente")
    nomes_depois = cursor.fetchall()
    print(f"   Nomes únicos depois: {len(nomes_depois)}")
    for nome in nomes_depois:
        print(f"      - {nome[0]}")
    print()

    # Salvar alterações
    conn.commit()
    conn.close()

    print("🎉 Banco de dados atualizado com sucesso!")
    print(f"   Total: {vendas_atualizadas + fiados_atualizados} registros normalizados")
    print()
    print("💡 Agora substitua o app.py pela versão corrigida e reinicie o servidor.")

if __name__ == '__main__':
    normalizar_nomes()
