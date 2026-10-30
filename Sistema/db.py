"""Acesso ao MySQL: uma conexão por consulta e parâmetros %s."""
import os
from datetime import date

import mysql.connector

CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Senai@118"),
    "database": os.getenv("DB_NAME", "assistencia_db"),
}


class ErroNegocio(Exception):
    """Erro de validação/regra de negócio, devolvido ao usuário em JSON com um status HTTP."""

    def __init__(self, mensagem, status=400):
        super().__init__(mensagem)
        self.mensagem, self.status = mensagem, status


def query(sql, params=()):
    """SELECT: devolve uma lista de dicionários com datas em formato ISO."""
    with mysql.connector.connect(**CONFIG) as con, con.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        return [
            {
                chave: valor.isoformat() if isinstance(valor, date) else valor
                for chave, valor in linha.items()
            }
            for linha in cur.fetchall()
        ]


def execute(sql, params=()):
    """INSERT/UPDATE/DELETE com commit. Devolve o id inserido (no INSERT)."""
    with mysql.connector.connect(**CONFIG) as con, con.cursor() as cur:
        cur.execute(sql, params)
        con.commit()
        return cur.lastrowid


def buscar_um(sql, params, mensagem):
    """Devolve a primeira linha da consulta ou erro 404 se não houver resultado."""
    linhas = query(sql, params)
    if not linhas:
        raise ErroNegocio(mensagem, 404)
    return linhas[0]


def bloquear_se_existir(sql, params, mensagem):
    """Se a consulta achar algum registro, erro 409 por duplicidade ou uso."""
    if query(sql, params):
        raise ErroNegocio(mensagem, 409)


def testar_conexao():
    return query("SELECT DATABASE() AS banco, VERSION() AS versao")[0]
