from ai_app import app, db
from datetime import datetime


class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(80), index=True, unique=False)
    song_name = db.Column(db.String(100), index=True, unique=True)
    song_text = db.Column(db.Text, index=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"This is song {self.song_name} from album {self.album} made by {self.artist}"

#
#with app.app_context():
     #db.create_all()