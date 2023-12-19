import requests
import base64

def get_spotify_track_id(song_title, artist_name, access_token):
    query = f"{song_title} artist:{artist_name}"
    response = requests.get(
        f"https://api.spotify.com/v1/search?q={query}&type=track",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    results = response.json()['tracks']['items']
    if results:
        return results[0]['id']  # returns the ID of the first matching track
    else:
        return None

def get_spotify_access_token(client_id, client_secret):
    # Encode the Client ID and Client Secret
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

    # Spotify Token URL
    token_url = "https://accounts.spotify.com/api/token"

    # Request Headers
    token_headers = {
        "Authorization": f"Basic {client_creds_b64}"  # Basic <base64 encoded client_id:client_secret>
    }

    # Request Body
    token_data = {
        "grant_type": "client_credentials"
    }

    # POST Request
    r = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = r.json()

    if r.status_code not in range(200, 299):
        raise Exception("Could not authenticate client")
    
    access_token = token_response_data['access_token']
    return access_token