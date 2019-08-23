from flask import Flask, g, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thisismypassword'

db = SQLAlchemy(app)

import models
from forms import Select_Movie

def get_form():
    if 'form' not in g:
        g.form = Select_Movie()
        movies = models.Movie.query.all()
        # Takes list of (value, label) pairs
        # The value will be sent as the form data
        g.form.movies.choices = [(movie.id, movie.title) for movie in movies]

    # TODO: Set the default selection on the form to the current movie being viewed

    return g.form

@app.route('/')
def root():
    return render_template('home.html', page_title="Home", form=get_form())

@app.route('/all_movies')
def all_movies():
    movies = models.Movie.query.all()
    return render_template('all_movies.html', page_title="All Movies", movies=movies, form=get_form())

@app.route('/movie/<int:id>')
def movie(id):
    movie = models.Movie.query.filter_by(id=id).first_or_404()
    title = movie.title
    return render_template('movie.html', page_title=title, movie=movie, form=get_form())

@app.route('/choose_movie', methods=['GET', 'POST'])
def choose_movie():
    form = get_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Since the value (in our case the movie.id) is the one sent through as form data
            # we can just grab it directly from the data object
            selected_movie_id = form.movies.data
            return redirect(url_for('movie', id=selected_movie_id))
        else:
            abort(404)
    # Not sure when this is actually triggered
    return render_template('choose_movie.html', title='Choose a movie', form=get_form())

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html', page_title="You've ventured too far...", form=get_form())

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)