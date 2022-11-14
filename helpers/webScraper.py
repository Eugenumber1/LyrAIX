import pandas as pd
import lyricsgenius

TOKEN = 'H89D3eV0IYOWGptlLMG4RFuTbmjPPSl6XwJ756OLd2tS56A3nbc17bwOIWcixQkK'

genius = lyricsgenius.Genius(TOKEN)

#artist = genius.search_artist("La Femme", max_songs=100, sort="popularity", include_features=True)
#for song in artist.songs:
    #print(song.lyrics)


def getLyrics(artist_name):
    df = pd.DataFrame(columns=["Artist", "Song", "Lyrics"])
    artist = genius.search_artist(artist_name, max_songs=100, sort="popularity", include_features=True)
    counter = len(df)
    for song in artist.songs:
        df.at[counter, "Artist"] = song.artist
        df.at[counter, "Song"] = song
        #df.at[counter, "Album"] = song.album
        df.at[counter, "Lyrics"] = song.lyrics
        counter += 1
    return df



#print(getLyrics("La Femme")["Lyrics"])

#getLyrics("La Femme").to_csv("/Users/zhenyabudnyk/PycharmProjects/LyrAIX/helpers/lyrics.csv")
