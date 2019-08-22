from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import models

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

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html', page_title="You've ventured too far...")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)