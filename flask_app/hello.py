from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '4829jfnwurduh4293k'
bootstrap = Bootstrap(app=app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['is_uoft'] = True if 'utoronto' in session['email'] else False
        return redirect((url_for('index')))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), is_uoft=session.get('is_uoft'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)