# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Avaliação contínua: Aula 030</h1><ul><li><a href="/">Home</a><li><a href="/user/Gabriel Jefferson/PT3025641/IFSP">Identificação</a><li><a href="/contextorequisicao">Contexto da requisição</a></li></ul>'

@app.route('/user/<name>/<prontuario>/<instituicao>')
def user(name, prontuario, instituicao):
    return '<h1>Avaliação contínua: Aula 030</h1><h2>Aluno: {}</h2><h2>Prontuário: {}</h2><h2>Instituição: {}</h2><p><a href="../../../">Voltar</a></p>'.format(name, prontuario, instituicao)

@app.route('/contextorequisicao')
def contextoRequisicao():
    user_agent = request.headers.get('User-Agent')
    ip_agent = request.remote_addr
    base_url = request.host
    return '<h1>Avaliação contínua: Aula 030</h1><h2>Seu navegador é: {}</h2><h2>O IP do computador remoto: {}</h2><h2>O host da aplicação é: {}</h2><p><a href="./">Voltar</a></p>'.format(user_agent, ip_agent, base_url)