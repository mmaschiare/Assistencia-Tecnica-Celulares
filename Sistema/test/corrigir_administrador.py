# -*- coding: utf-8 -*-
"""Redefine a senha do administrador usando a configuração e o esquema do sistema."""
import mysql.connector

from autenticacao import gerar_hash
from db import CONFIG

SENHA_NOVA = "assistencia@123"


def corrigir_administrador():
    hash_novo = gerar_hash(SENHA_NOVA)

    with mysql.connector.connect(**CONFIG) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "UPDATE usuarios SET senha_hash = %s WHERE login = %s",
                (hash_novo, "admin"),
            )

            if cursor.rowcount == 0:
                cursor.execute(
                    "INSERT INTO usuarios (nome, login, senha_hash) VALUES (%s, %s, %s)",
                    ("Administrador", "admin", hash_novo),
                )
                resultado = "criado"
            else:
                resultado = "atualizado"

        conexao.commit()

    print(f"Usuário administrador {resultado}.")
    print("Login: admin")
    print("Execute o login usando a senha configurada em SENHA_NOVA.")


if __name__ == "__main__":
    corrigir_administrador()
