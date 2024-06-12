import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import random

CLIENT_ID = None
CLIENT_SECRET = None
REDIRECT_URI = 'http://localhost:5000' # the spotipy library sets up a webserver on this port

# using authorization code flow, so a OAutho manager is required
# Authenticate with Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read user-read-recently-played'  # requesting access to top songs, artists, and recently played tracks
    )
)

# Setting up the Streamlit page
st.set_page_config(page_title="Spotify Analysis", page_icon=':musical_note:')
st.title("Your Spotify Analysis")
st.write('Discover insights about your spotify listening habits.')

# Retrieve the three most recently played tracks
recently_played = sp.current_user_recently_played(limit=3)
recent_tracks = [(track['track']['name'], track['track']['album']['images'][0]['url']) for track in recently_played['items']]

# Display the three most recently played tracks
st.subheader('Recently Played Tracks')
cols = st.columns(len(recent_tracks))
for col, (name, img_url) in zip(cols, recent_tracks):
    with col:
        st.image(img_url, use_column_width=True, caption=name)

# Retrieve top 5 artists
top_artists = sp.current_user_top_artists(limit=5, time_range='short_term')
artist_names = [artist['name'] for artist in top_artists['items']]
artist_images = [artist['images'][0]['url'] if artist['images'] else None for artist in top_artists['items']]

# Display top artists with profile pictures
st.subheader('Top 5 Artists')
cols = st.columns(len(artist_names))
for col, (name, img_url) in zip(cols, zip(artist_names, artist_images)):
    with col:
        if img_url:
            st.image(img_url, width=100, use_column_width=True, caption=name, output_format="PNG")


# Retrieve top 5 tracks
top_tracks = sp.current_user_top_tracks(limit=5, time_range='short_term')
track_ids = [track['id'] for track in top_tracks['items']]  # Getting the ID for each individual track
audio_features = sp.audio_features(track_ids)  # Getting features for the track (e.g. danceability, loudness)

# Create DataFrame for track audio features
df_tracks = pd.DataFrame(audio_features)
df_tracks['track_name'] = [track['name'] for track in top_tracks['items']]
df_tracks = df_tracks[['track_name', 'danceability', 'energy', 'valence']]
df_tracks.set_index('track_name', inplace=True)  # Can retrieve rows according to track name

# Display audio features for top tracks
st.subheader('Audio Features for Top Tracks')
st.bar_chart(df_tracks, height=500)

# Get recommendations based on top 5 tracks
recommendations = sp.recommendations(seed_tracks=track_ids, limit=5)
rec_tracks = [(track['name'], track['album']['images'][0]['url']) for track in recommendations['tracks']]

# Display recommended tracks
st.subheader('Recommended Tracks')
cols = st.columns(len(rec_tracks))
for col, (name, img_url) in zip(cols, rec_tracks):
    with col:
        st.image(img_url, use_column_width=True, caption=name)

# Function to fetch related artists for a given artist ID
def get_related_artist(artist_id):
    related_artists = sp.artist_related_artists(artist_id)
    if related_artists['artists']:
        random_index = random.randint(0, len(related_artists['artists']) - 1)
        return related_artists['artists'][random_index]  # Return a random related artist
    else:
        return None

# Get recommendations for artists based on top artists
artist_ids = [artist['id'] for artist in top_artists['items']]
recommended_artists = []

# Fetch related artists for each recommended artist
for artist_id in artist_ids:
    related_artist = get_related_artist(artist_id)
    if related_artist:
        recommended_artists.append(related_artist)

# Display recommended artists with profile pictures
st.subheader('Recommended Artists')
cols = st.columns(len(recommended_artists))
for col, artist in zip(cols, recommended_artists):
    with col:
        st.image(artist['images'][0]['url'], width=100, use_column_width=True, caption=artist['name'], output_format="PNG")