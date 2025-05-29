import requests
from requests_oauthlib import OAuth2Session

## So im a newer dev, and wont lie had ai help a bit, so ill go through and explain what everything is doing to help me understand whats going on.

client_id = 'paste client id here'
client_secret = 'i think this is for authentication stuff'
redirect_uri = 'copy and paste something here too'
tag = 'what music do you wanna search for?'
limit = 100

authorization_base_url = 'https://soundcloud.com/connect'
token_url = 'https://api.soundcloud.com/oauth2/token'


 #Grabbing the URL and opening up an OAuth2Session for the user to give authorization for the app to make a playlist on their account
soundcloud = OAuth2Session(client_id, redirect_uri=redirect_uri, scope='non-expiring')
authorization_url, state = soundcloud.authorization_url(authorization_base_url)

print('Go to:', authorization_url)

redirect_response = input('Paste the full redirect URL here: ')
#Token for authorization, which we now have!
token = soundcloud.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)



def search_tracks(tag, limit=100):
    #Basic stuff to define where we get the tracks, and what we are looking for
    url = f"https://api-v2.soundcloud.com/search/tracks"
    params = {
        'q':tag,
        'client_id': client_id,
        'limit': limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['collection']

#Pulling the tracks by title and URL to add to playlist
tracks = search_tracks(tag, limit)
for t in tracks:
    print(t['title'], '-', t['permalink-url'])


def create_playlist(oauth_session, track_ids, title='My Playlist'):
    payload = {
        'playlist': {
            'title': title,
            'sharing': 'public',
            'tracks': [{'id': tid} for tid in track_ids]
        }
    }
    #API to make the playlist
    response = oauth_session.post('https://api.soundcloud.com/playlists', json=payload)
    response.raise_for_status()
    return response.json()

track_ids = [t['id'] for t in tracks]

#Playlist is created here
playlist = create_playlist(soundcloud, track_ids, title='Chill Tracks Bot')
print('Playlist created:', playlist['permalink_url'])
