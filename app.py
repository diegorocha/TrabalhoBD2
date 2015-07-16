#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Flask, render_template, jsonify, request
from json import loads
import controller

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('list.htm', list=controller.list_all())


@app.route('/add')
def list_all():
    return render_template('add.htm')


@app.route('/save', methods=['POST'])
def save():
    usuario = loads(request.form['data'])
    r = controller.save(usuario)
    return jsonify(result=r[0], message=r[1])


@app.route('/cep/<int:n_cep>', methods=['GET', 'POST'])
def get_cep(n_cep):
    return jsonify(controller.get_logradouro(n_cep))

if __name__ == '__main__':
    app.run()
