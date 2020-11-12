import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask import Flask, render_template, redirect, url_for, request, flash
from random import choice
import os

from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(app.root_path,
                                                                                                      'Quote.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "h1Maw~}NDbm~oTEX"
app.config['DEBUG'] = True
db = SQLAlchemy(app)

@click.command(name='create_table')
@with_appcontext
def create_tables():
    db.create_all()


class Quote(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True)

    def __repr__(self):
        return self.text


@app.route('/', methods=['POST', 'GET'])
def index():
    quote = choice(Quote.query.all())
    return render_template("index.html", title='Ауф-цитатник', quote=quote)


@app.route('/new_quote')
def new_quote():
    return redirect(url_for('index'))


@app.route('/add_quote', methods=['POST', 'GET'])
def add_quote():
    if request.method == "POST":
        if len(request.form['quote']) > 10:
            try:
                q = Quote(text=request.form['quote'])
                db.session.add(q)
                db.session.flush()
                db.session.commit()
                flash("Цитата отправлена", category='success')
            except SQLAlchemyError:
                db.session.rollback()
                flash("Цитата не отправлена", category='error')
        else:
            flash("Цитата не отправлена", category='error')

    return render_template('add_quote.html', title='Новая цитата')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html')


if __name__ == "__main__":
    app.run(debug=True)
