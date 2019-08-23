from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thisismypassword'

db = SQLAlchemy(app)

import models
from forms import Select_Movie

@app.route('/')
def root():
    return render_template('home.html', page_title="Home")

@app.route('/all_movies')
def all_movies():
    movies = models.Movie.query.all()
    return render_template(
        'all_movies.html',
        page_title="All Movies",
        movies=movies)

@app.route('/movie/<int:id>')
def movie(id):
    movie = models.Movie.query.filter_by(id=id).first_or_404()
    title = movie.title
    return render_template('movie.html', page_title=title, movie=movie)

@app.route('/choose_movie', methods=['GET', 'POST'])
def choose_movie():
    form = Select_Movie()
    movies = models.Movie.query.all() # Move this out into a global later?
    # Takes list of (value, label) pairs
    # The value will be sent as the form data
    form.movies.choices = [(movie.id, movie.title) for movie in movies]
    if request.method == 'POST':
        if form.validate_on_submit():
            # Since the value (in our case the movie.id) is the one sent through as form data
            # we can just grab it directly from the data object
            selected_movie_id = form.movies.data
            return redirect(url_for('movie', id=selected_movie_id))
        else:
            abort(404)
    return render_template('choose_movie.html', title='Choose a movie', form=form)

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html', page_title="You've ventured too far...")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)