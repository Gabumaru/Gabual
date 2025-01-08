from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Role
from ..email import send_email, send_simple_message
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    users = User.query.all()
    session['email_sent'] = False
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            role = Role.query.filter_by(name="User").first()
            user = User(username=form.name.data, role=role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            print('FLASKY_ADMIN: ' + str(current_app.config['FLASKY_ADMIN']), flush=True)
            if current_app.config['FLASKY_ADMIN']:
                #send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
                print('Enviando mensagem...', flush=True)
                print(form.email.data)
                send_simple_message([current_app.config['FLASKY_ADMIN'], form.email.data, "flaskaulasweb@zohomail.com"], 'Novo usuário', form.name.data)
                print('Mensagem enviada...', flush=True)
                session['email_sent'] = True  # Marca como enviado
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))

    email_sent = session.pop('email_sent', False)
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False), users=users, email_sent=email_sent)