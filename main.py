from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()


configure()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
Bootstrap5(app)
db = SQLAlchemy()
db.init_app(app)

headers = {
    "accept": "application/json",
    "Authorization": os.getenv("bearer")
}


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


class AddMovieForm(FlaskForm):
    movie = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_movies = db.session.query(Movie).order_by(Movie.rating.desc()).all()
    for rank, movie in enumerate(all_movies, start=1):
        movie.ranking = rank
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route('/add_to_db/<int:movie_id>')
def add_to_db(movie_id):
    movie_data = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US",
                              headers=headers).json()
    new_movie = Movie(
        title=movie_data["title"],
        img_url=f"https://image.tmdb.org/t/p/original{movie_data['poster_path']}",
        year=movie_data["release_date"].split("-")[0],
        description=movie_data["overview"]
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=new_movie.id))


@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form)


@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=["GET", "POST"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_name = form.movie.data
        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1",
            headers=headers).json()
        movie_list = [(movie["title"], movie["release_date"], movie["id"]) for movie in response["results"]]
        return render_template('select.html', movies=movie_list)
    return render_template('add.html', form=form)


@app.route('/select')
def select():
    return render_template('select.html')


if __name__ == '__main__':
    app.run(debug=True)
