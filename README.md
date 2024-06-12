# Personal-Spotify-Dashboard
Using the Spotify API and Python with its Spotipy and Streamlit libraries, the user's recently played tracks, along with the top five artists and songs are shown, and recommended artists and tracks are also displayed

In the script, 
CLIENT_ID = None
CLIENT_SECRET = None

To obtain the client ID and secret, the user must create an app in the Spotify for developers' website after logging in with the account they want to analyze.
After doing so, they can go to the settings to find both.

![image](https://github.com/nasir-syed/Personal-Spotify-Dashboard/assets/172494217/deaf2e82-8e26-4343-84da-a5dac713a656)
![image](https://github.com/nasir-syed/Personal-Spotify-Dashboard/assets/172494217/b23510a2-196f-46a8-b649-076bf8953d58)

After obtaining the client ID and secret, replace the variables with the actual value as a string.

The script is run using the following command in the terminal:
streamlit run <filepath> --server.headless True
