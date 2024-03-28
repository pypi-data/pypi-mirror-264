from client import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Spotify app's client ID and client secret
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET =  os.getenv("CLIENT_SECRET")

def main():
   spy = Client(CLIENT_ID,CLIENT_SECRET)
   artist_data = spy.search_for_artist("J. Cole")
   print(artist_data)
   top_ten = spy.get_top_ten("J. Cole")
   print(top_ten)
   track = spy.get_song("Wet Dreamz")
   print(track)
   analysis = spy.analyze("Hello Lionel")
   print(analysis)
   artist_albums = spy.get_artist_albums("nonexist_artist_name_1234567")
   print(artist_albums)


if __name__ == "__main__":
    main()
