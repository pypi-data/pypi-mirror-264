import requests

class Client:
    # Spotify API endpoints
    AUTH_URL = "https://accounts.spotify.com/api/token"
    BASE_URL = "https://api.spotify.com/v1/"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def authenticate(self):
        # Request an access token
        auth_response = requests.post(self.AUTH_URL, data={
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })

        # Convert the response to JSON
        auth_response_data = auth_response.json()

       
        #Save the access token
        access_token = auth_response_data['access_token']

        return access_token
            
    def search(self, headers,name,keyword):

        response = requests.get(self.BASE_URL + f'search?q={keyword}:{str.lower(name)}&type={keyword}', headers=headers)

        # Convert the response to JSON
        response_data = response.json()

        # # Get the album's Spotify ID
        # album_id = response_data[keyword+"s"]['items'][0]['id']
        plural = keyword+"s"

        # Get the artist's Spotify ID
        if plural in response_data and 'items' in response_data[plural] and response_data[plural]['items']:
            artist_id = response_data[plural]['items'][0]['id']
            return artist_id
        else:
            return None

        
    
    

    def get_top_ten(self, artist):
        # retArray = []
        retStr = ""

        access_token = self.authenticate()

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        artist_id = self.search(headers, artist, "artist")

        # Use the artist's Spotify ID to get their top tracks
        response = requests.get(self.BASE_URL + 'artists/' + artist_id + '/top-tracks?country=US', headers=headers)

        # Error handling
        if response.status_code != 200:
            print(f"The artist request was invalid, error:{response.status_code}")
            return
        

        # Convert the response to JSON
        response_data = response.json()

        # Print the names of the artist's top 10 tracks
        for i, track in enumerate(response_data['tracks'][:10]):
            # retArray.append(track['name'])
            retStr = retStr + f"{i+1}. {track['name']}\n"
            #print(f"{i+1}. {track['name']}")

        
        # print(retArray)
        return retStr

    # def get_album(self, album):
    #     retArray = []

    #     access_token = self.authenticate()

    #     headers = {
    #     'Authorization': 'Bearer {token}'.format(token=access_token)
    #     }

    #     album_id = self.search(headers, album, "album")

    #     # Use the album's Spotify ID to get more information
    #     response = requests.get(self.BASE_URL + 'albums/' + album_id, headers=headers)

    #     # Error handling
    #     if response.status_code != 200:
    #         print(f"The album request was invalid, error:{response.status_code}")
    #         return

    #     # Convert the response to JSON
    #     response_data = response.json()

    #     # Print the names of the artist's top 10 tracks
    #     for track in response_data['tracks']['items']:
    #         retArray.append({'name' : track['name'], "milliseconds": track['duration_ms'], "id": track['duration_ms']})
    #         #print(f"{i+1}. {track['name']}")

    #     # print(retArray)
    #     return retArray

    def get_song(self, song):

        access_token = self.authenticate()

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        song_id = self.search(headers, song, "track")

        # Use the song's Spotify ID to get more information
        response = requests.get(self.BASE_URL + 'tracks/' + song_id, headers=headers)

        # Error handling
        if response.status_code != 200:
            print(f"The song request was invalid, error:{response.status_code}")
            return

        # Convert the response to JSON
        response_data = response.json()    

        return [response_data['name'],response_data['duration_ms']]
    
    def get_track_id(self, song):
        access_token = self.authenticate()
        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        response = requests.get(self.BASE_URL + f'search?q=track:{str.lower(song)}&type=track',headers=headers)
        response_data = response.json()
        # print(response_data['tracks']['items'])
        # Get the song's Spotify ID
        if response_data['tracks']['items'] == []:
            return "No such track ID found"
        elif song == "":
            # print("Please enter the name of a song.")
            return "Please enter the name of a song."
        else: song_id = response_data['tracks']['items'][0]['id']
        return song_id
    
    

    def analyze(self, song):
        access_token = self.authenticate()

        headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
        }

        if self.get_track_id(song) == "No such track ID found":
            # print("Invalid track ID")
            return "Invalid track ID"
        elif song == "":
            # print("Please enter the name of a song.")
            return "Please enter the name of a song."
        else:
            song_id = self.get_track_id(song)
            #print(song_id)
            response = requests.get(self.BASE_URL + 'tracks/' + song_id, headers=headers)
            response_data = response.json()
            # print(response_data["artists"])
            print(f"{response_data['name']} by {response_data['artists'][0]['name']}:")

            #Use the song's Spotify ID to get their audio features
            features_response = requests.get(self.BASE_URL + 'audio-features/' + song_id, headers=headers)
            features_response_data = features_response.json()
            # print(features_response_data)

            feature_list = ''
            for feature in features_response_data:
                # print(f"{feature}: {features_response_data[feature]}")
                feature_list = feature_list + f"{feature}: {features_response_data[feature]}\n"
            # print(feature_list)
            return feature_list

    def search_for_artist(self, artist_name):
        """
            Search for an artist by name.

             Args:

            -artist_name (str): the name of the artist to search for.

            Returns:

            -dict: About the artist.

        """   


        access_token = self.authenticate()

        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
            }

        response = requests.get(self.BASE_URL + 'search?q=' + artist_name + '&type=artist', headers=headers)

        if response.status_code == 200:
            artist_data = response.json()['artists']['items'][0]
            return artist_data

        else:
            print("Failed to get artist's informstion: {response.status_code}")
            return None
        
    def get_artist_albums(self, artist):
        access_token = self.authenticate()
        headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
        artist_id = self.search(headers, artist, "artist")
        if artist_id:
            response = requests.get(self.BASE_URL + 'artists/' + artist_id + '/albums', headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                
                if 'items' in response_data:
                    albums = [album for album in response_data['items'] if album.get('album_type') == 'album']
                    album_names = [album["name"] for album in albums]
                    return album_names
                    
                else:
                    print("No albums found for the artist.")
                    return []
            else:
                print(f"Failed to fetch albums for artist {artist_id}. Status code: {response.status_code}")
                return []
        else:
            print(f"No artist found with name '{artist}'")
            return []