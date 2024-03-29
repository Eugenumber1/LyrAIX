from flask import Flask, url_for, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from helpers import webScraper
import lyricsgenius
import pandas as pd
from helpers.NeuralNetwork import SongCreator

# from models import *
# from table import *

# ------------ ATOMIC VARS ---------------

TOKEN = 'H89D3eV0IYOWGptlLMG4RFuTbmjPPSl6XwJ756OLd2tS56A3nbc17bwOIWcixQkK'

genius = lyricsgenius.Genius(TOKEN)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///song.db'
db = SQLAlchemy(app)


# ------------DATABASE MODEL-----------

class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(80), index=True, unique=False)
    album = db.Column(db.String(80), index=True, unique=False)
    song_name = db.Column(db.String(100), index=True, unique=True)
    song_text = db.Column(db.Text, index=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"This is song {self.song_name} made by {self.artist}"


# -----------FORM class -------------

class CommentForm(FlaskForm):
    artist = StringField("Artist Name")
    submit = SubmitField("Search for Artist")


# --------------- API -------------------

@app.route('/', methods=['POST', 'GET'])  # url for my app
def home():
    return render_template("home.html")


@app.route('/search_artist', methods=["POST", "GET"])
def search_artist():
    if request.method == "POST":
        artist = request.form['artist-search']
        songs = Song.query.all()
        artists = set()
        for song in songs:
            artists.add(song.artist)
        if artist in artists:
            return redirect(url_for("artist", artist_name=artist, _external=True, _scheme="http"))
        elif artist not in artists:
            artist_found = genius.search_artist(artist, max_songs=10, sort="title", include_features=True)
            for song in artist_found.songs:
                if song.lyrics != "" and song.title != "":
                    try:
                        new_song = Song(artist=artist, song_name=song.title, song_text=song.lyrics)
                        print(new_song.artist)
                        db.session.add(new_song)
                    except:
                        return 'There was an issue with adding the song'
            db.session.commit()
            return redirect(url_for("artist", artist_name=artist, _external=True, _scheme="http"))
    else:
        return render_template('search_artist.html')


@app.route("/artist/<string:artist_name>", methods=["POST", "GET"])
def artist(artist_name=None):
    # print(artist_name)
    songs = Song.query.filter_by(artist = artist_name).all() # Book.query.filter(Book.year = 2020).all()
    total = 0
    number = len(songs)
    for song in songs:
        total += len(song.song_text)
    avarage = total // number
    print(avarage)
    # print(len(songs))
    # for song in songs:
    #     print(song.song_id)
    if request.method == "POST":
        sc = SongCreator(songs, avarage)
        #new_song_name = sc.generate_title()
        new_song = sc.generate_song()
        song_to_add = Song(artist=artist_name, song_text=new_song)
        try:
            db.session.add(song_to_add)
        except:
            return "There was an issue with adding newly generated song"
        db.session.commit()
        song_id = song_to_add.song_id
        print(song_id)

        return redirect(url_for("generate", artist_name=artist, new_song_id=song_id, _external=True, _scheme="http"))
    else:
        return render_template("artist.html", artist=artist_name, songs=songs)



@app.route("/artist/<string:artist_name>/<int:new_song_id>")
def generate(artist_name, new_song_id):
   song = Song.query.get_or_404(new_song_id)
   return render_template("new_song.html", artist=artist_name, new_song=song.song_text)


# @app.route("/scrape/<artist_name>", methods=["POST", "GET"])
# def artist(artist_name):
#     artist = genius.search_artist(artist_name, max_songs=3, sort="title", include_features=True)
#     for song in artist.songs:
#         new_song = Song(artist=artist_name, lyrics=song.lyrics)
#         print(new_song.artist)
#         try:
#             db.session.add(new_song)
#         except:
#             return 'There was an issue with adding the song'
#     db.session.commit()
#     return redirect('/scrape/<artist_name>')


if __name__ == "__main__":
    app.run(debug=True)


