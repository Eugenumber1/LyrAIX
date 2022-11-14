from flask import Flask, url_for, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from helpers import webScraper

import lyricsgenius
import pandas as pd
TOKEN = 'H89D3eV0IYOWGptlLMG4RFuTbmjPPSl6XwJ756OLd2tS56A3nbc17bwOIWcixQkK'

genius = lyricsgenius.Genius(TOKEN)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    artist = db.Column(db.String(200), nullable=False)
    lyrics = db.Column(db.String(), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Song %r>' % self.id

print(Song.lyrics)



@app.route('/', methods=['POST', 'GET']) # url for my app
def index():
    if request.method == 'POST':
        artist_name = request.form['artist-search']
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
        songs = Song.query.order_by(Song.date_created).all() # query all tasks and order them by date
        return render_template('home.html', songs=songs)



if __name__=="__main__":
    app.run(debug=True)