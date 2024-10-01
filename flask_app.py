# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, make_response, redirect, abort

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!'.format(name)

@app.route('/contextorequisicao')
def contextoRequisicao():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

@app.route('/codigostatusdiferente')
def codigoStatus():
    return '<p>Bad Request</p>', 400


@app.route('/objetoresposta')
def objetoResposta():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/redirecionamento')
def redirecionamento():
    return redirect('https://ptb.ifsp.edu.br')


@app.route('/abortar')
def abortar():
    abort(404)