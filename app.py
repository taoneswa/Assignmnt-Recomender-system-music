import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Display the names at the top of the UI
st.header('Music Recommender System Assignment')
st.markdown("""
**Team Members:**
- Priviledge Murombeka R207113W HDSC
- Peter Mutsiwa R195820R CTHSC
- Taoneswa Kasirai R204450W HAI
- Takunda Kondo R195926T CTHSC
""")

# Spotify API credentials
CLIENT_ID = "496be5df71524c888f6560588f5ab008"
CLIENT_SECRET = "7921e2d638c64c4899831cbd32873f57"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"


def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        # Fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(
            get_song_album_cover_url(music.iloc[i[0]].song, artist)
        )
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters


music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
        
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])

    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
        
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
        
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
