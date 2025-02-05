import os
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from datetime import datetime
import requests

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'flaskaulasweb@zohomail.com'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# Novo modelo Ocorrencia
class Ocorrencia(db.Model):
    __tablename__ = 'ocorrencias'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    data_ocorrencia = db.Column(db.DateTime, nullable=False)
    disciplina = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Ocorrencia {self.id} - {self.descricao}>'


# Formulário para cadastrar ocorrências
class OcorrenciaForm(FlaskForm):
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    disciplina = StringField('Disciplina', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Ocorrencia=Ocorrencia)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Alterado para 'não_disponivel' (nova página de cadastro)
@app.route('/nao_disponivel', methods=['GET', 'POST'])
def nao_disponivel():
    form = OcorrenciaForm()
    if form.validate_on_submit():
        ocorrencia = Ocorrencia(
            descricao=form.descricao.data,
            disciplina=form.disciplina.data,
            data_ocorrencia=datetime.utcnow()  # Grava a data atual
        )
        db.session.add(ocorrencia)
        db.session.commit()
        return redirect(url_for('nao_disponivel'))  # Redireciona após o cadastro

    # Pega todas as ocorrências cadastradas e ordena por data
    ocorrencias = Ocorrencia.query.order_by(Ocorrencia.data_ocorrencia.desc()).all()
    
    return render_template('não_disponivel.html', form=form, ocorrencias=ocorrencias)


# Rota para visualizar todas as ocorrências
@app.route('/ocorrencias', methods=['GET'])
def listar_ocorrencias():
    ocorrencias = Ocorrencia.query.order_by(Ocorrencia.data_ocorrencia.desc()).all()
    return render_template('ocorrencias.html', ocorrencias=ocorrencias)


if __name__ == '__main__':
    app.run(debug=True)
