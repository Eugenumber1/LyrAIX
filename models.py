from ai_app import app, db
from datetime import datetime


class Artist(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(100), index=True, unique=True)
    albums = db.relationship("Album", backref='artist', lazy='dynamic')
    songs = db.relationship("Song", backref="artist", lazy="dynamic")


    def __repr__(self):
        return f"This is artist number {self.artist_id} and his name is {self.artist_name}"



class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(100), index=True, unique=True)
    artist = db.Column(db.Integer, db.ForeignKey(Artist.artist_id))
    songs = db.relationship("Song", backref='album', lazy='dynamic')

    def __repr__(self):
        return f"This is an album {self.album_name} made by {self.artist.artist_name}"


class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Integer, db.ForeignKey(Artist.artist_id))
    album = db.Column(db.Integer, db.ForeignKey(Album.album_id))
    song_name = db.Column(db.String(100), index=True, unique=True)
    song_text = db.Column(db.Text, index=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"This is song {self.song_name} from album {self.album.album_name} made by {self.artist.artist_name}"


#with app.app_context():
    #db.create_all()