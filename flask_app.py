
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>/<prontuario>/<instituicao>')
def user(name, prontuario, instituicao):
    return render_template('user.html', name=name, prontuario=prontuario, instituicao=instituicao)

@app.route('/contextorequisicao/<name>')
def contextorequisicao(name):
    navegador=request.headers.get('User-Agent')
    ip_agent=request.remote_addr
    base_url=request.host
    return render_template('contextorequisicao.html', name=name, navegador=navegador, ip_agent=ip_agent, base_url=base_url)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500