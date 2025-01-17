import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Class %r>' % self.name

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ClassForm(FlaskForm):
    name = StringField('Qual é o nome do curso?', validators=[DataRequired()])
    description = TextAreaField('Descrição (250 caracteres)')
    submit = SubmitField('Cadastrar')



@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow());

@app.route('/professores', methods=['GET', 'POST'])
def professores():
    return render_template('nao_disponivel.html', current_time=datetime.utcnow());

@app.route('/disciplinas', methods=['GET', 'POST'])
def disciplinas():
    return render_template('nao_disponivel.html', current_time=datetime.utcnow());

@app.route('/alunos', methods=['GET', 'POST'])
def alunos():
    return render_template('nao_disponivel.html', current_time=datetime.utcnow());


@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    form = ClassForm()
    class_all = Class.query.all();
    if form.validate_on_submit():

        curso = Class(name=form.name.data, description=form.description.data);
        db.session.add(curso)
        db.session.commit()

        return redirect(url_for('cursos'))
    return render_template('cursos.html', form=form,
                           class_all=class_all);

@app.route('/ocorrencias', methods=['GET', 'POST'])
def ocorrencias():
    return render_template('nao_disponivel.html', current_time=datetime.utcnow());