#script to add test data
from ai_app import db, app, Song
#from table import Song



s1 = Song(song_id = 1, artist = "Franks Sinatra", album = "good", song_name = "Fly me to the Moon", song_text="hey")
s2 = Song(song_id = 2, artist = "David Bowie", album = "good", song_name = "Space Oddity", song_text="yooo")
s3 = Song(song_id = 3, artist = "Sting", album = "good", song_name = "Walking on the Moon", song_text="nice")
s4 = Song(song_id = 4, artist = "Nick Cave & The Bad Seeds", album = "good", song_name = "Rings of Saturn", song_text="cool")
s5 = Song(song_id = 5, artist = "Babylon Zoo", album = "good", song_name = "Spaceman", song_text="yesss")


with app.app_context():
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    db.session.add(s5)
    db.session.commit()