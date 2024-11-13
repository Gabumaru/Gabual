
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    name = StringField('Informe o seu nome', validators= [DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators= [DataRequired()])
    instituicao = StringField('Informe a sua Instituição de ensino:', validators= [DataRequired()])
    disciplina = SelectField('Informe a sua disciplina:', choices=[('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('Gestão de projetos', 'Gestão de projetos')], validators= [DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chave Secreta'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = StudentForm()
    ip_agent=request.remote_addr
    base_url=request.host
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome!')
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['instituicao'] = form.instituicao.data
        session['disciplina'] = form.disciplina.data
        session['ip_agent'] = ip_agent
        session['base_url'] = base_url
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), surname=session.get('surname'), instituicao=session.get('instituicao'), disciplina=session.get('disciplina'), ip_agent=session.get('ip_agent'), base_url=session.get('base_url'), current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500