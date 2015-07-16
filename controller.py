#!/usr/bin/env python
# -*- coding: utf-8 -*

import psycopg2

__CONN_STRING__ = "postgresql://postgres:postgres@localhost:5432/trabalhobd2"


def get_connection():
    return psycopg2.connect(__CONN_STRING__)


def get_logradouro(cep):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""select cep, nome, bairro, cidade, uf
                   from logradouro where cep = %d""" % cep)
    rows = cur.fetchall()
    logradouro = {}
    for row in rows:
        logradouro['cep'] = row[0]
        logradouro['nome'] = row[1].decode('utf-8')
        logradouro['bairro'] = row[2].decode('utf-8')
        logradouro['cidade'] = row[3].decode('utf-8')
        logradouro['uf'] = row[4]
    return logradouro


def save(usuario):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""insert into usuario(nome, cpf, sexo, telefone) values
                     (%(nome)s, %(cpf)s, %(sexo)s, %(telefone)s)
                     returning id""", usuario)
        usuario_id = cur.fetchone()[0]
        for endereco in usuario['enderecos']:
            endereco['usuario_id'] = usuario_id
            cur.execute("""insert into endereco_usuario
                        (usuario_id, cep, numero, complemento) values
                        (%(usuario_id)s, %(cep)s, %(numero)s,
                        %(complemento)s)""", endereco)
        conn.commit()
        return (True, '')
    except Exception, e:
        conn.rollback()
        return (False, str(e))


def list_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select id, nome, cpf, sexo, telefone from usuario")
    rows = cur.fetchall()
    usuarios = []
    for row in rows:
        usuario = {}
        usuario['id'] = row[0]
        usuario['nome'] = row[1].decode('utf-8')
        usuario['cpf'] = row[2]
        usuario['sexo'] = row[3]
        usuario['telefone'] = row[4]
        usuario['enderecos'] = []
        curEndereco = conn.cursor()
        curEndereco.execute("""select e.id, l.nome as logradouro, e.numero,
                               e.complemento, l.cep, l.bairro, l.cidade, l.uf
                               from endereco_usuario e
                               inner join logradouro l on (l.cep = e.cep)
                               where e.usuario_id = %d""" % usuario['id'])
        enderecos = curEndereco.fetchall()
        for e in enderecos:
            endereco = {}
            endereco['id'] = e[0]
            endereco['logradouro'] = e[1].decode('utf-8')
            endereco['numero'] = e[2]
            endereco['complemento'] = e[3].decode('utf-8')
            endereco['cep'] = e[4]
            endereco['bairro'] = e[5].decode('utf-8')
            endereco['cidade'] = e[6].decode('utf-8')
            endereco['uf'] = e[7]
            usuario['enderecos'].append(endereco)
        usuarios.append(usuario)
    return usuarios
