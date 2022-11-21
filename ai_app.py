from flask import Flask, url_for, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from helpers import webScraper
import lyricsgenius
import pandas as pd

# ------------ ATOMIC VARS ---------------

TOKEN = 'H89D3eV0IYOWGptlLMG4RFuTbmjPPSl6XwJ756OLd2tS56A3nbc17bwOIWcixQkK'

genius = lyricsgenius.Genius(TOKEN)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)
#app.config["SECRET_KEY"] = "mysecret"

# -----------FORM class -------------

class CommentForm(FlaskForm):
  artist = StringField("Artist Name")
  submit = SubmitField("Search for Artist")

# ------------- DATABASE CLASS --------------

class Song(db.Model):

    __tablename__ = "Songs"

    id = db.Column("user id", db.Integer, primary_key=True, unique=True)
    artist = db.Column("artist name", db.String(200), nullable=False)
    lyrics = db.Column("lyrics of the song", db.String(), nullable=False, unique=True)
    date_created = db.Column("date created", db.DateTime, default=datetime.utcnow)

    def __init__(self, artist, lyrics):
        self.artist = artist
        self.lyrics = lyrics

    def __repr__(self):
        return  f" song id - {id} "

# --------------- API -------------------

@app.route('/', methods=['POST', 'GET']) # url for my app
def home():
    return render_template("home.html")


@app.route('/search_artist', methods=["POST", "GET"])
def search_artist():
    if request.method =="POST":
        artist = request.form['artist-search']
        songs = Song.query.all()
        artists = set()
        for song in songs:
            artists.add(song.artist)
            print(song.artist)
        if artist in artists:
            return redirect(url_for("artist", artist_name=artist, _external=True, _scheme="https"))
        elif artist not in artists:
            return redirect(url_for("scrape_artist", artist_name=artist, _external=True, _scheme="https"))
    else:
        return render_template('search_artist.html')



@app.route("/artist/<artist_name>", methods=["POST", "GET"])
def artist(artist_name):
    songs = Song.query.get_or_404(artist_name)
    if request.method =="POST":
        pass
    else:
        render_template("artist.html", artist=artist_name, songs=songs)











if __name__=="__main__":
    app.run(debug=True)


"""
    if request.method == 'POST':
        artist_name = request.form['artist-search']
        for i in Song.query.filter(Song.artist == artist_name):
            print(i)
        if artist_name not in Song.query.filter(Song.artist == artist_name):
            artist = genius.search_artist(artist_name, max_songs=3, sort="title", include_features=True)
            for song in artist.songs:
                new_song = Song(artist=artist_name, lyrics=song.lyrics)
                print(new_song.artist)
                try:
                    db.session.add(new_song)
                except:
                    return 'There was an issue with adding the song'
            db.session.commit()
            return redirect('/')

    else:
        songs = Song.query.order_by(Song.lyrics).all() # query all songs
        return render_template('home.html', songs=songs)
"""