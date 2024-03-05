import csv
import json
import os
import random
import re
import time
import warnings
from urllib.parse import urljoin

import keyboard
import numpy as np
import pandas as pd
import requests
import spotipy
import streamlit as st
import yt_dlp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp.postprocessor import MetadataParserPP
from scripts.html_templates import css
from dotenv import load_dotenv



warnings.filterwarnings('ignore')

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
OUTPUT_FILE_NAME = "test.csv"
print(CLIENT_ID)
print(CLIENT_SECRET)



def calculate_score(track, artist, duration, name_found, duration_found):
    track = track.lower().split(" ")
    artist = artist.lower().split(" ")
    score = 0
    if any(keyword in name_found.lower() for keyword in track):
        score += 1
    if any(keyword in name_found.lower() for keyword in artist):
        score += 1
    keywords = ["lyrics", "extended", "audio"]
    if any(keyword in name_found.lower() for keyword in keywords):
        score += 2

    return score


def next_step():
    print("User Clicked---------------------------------------")
    print("Selected:" + str(st.session_state.selected))
    sel = st.session_state.selected.split(" ")
    print(sel)
    track_df = pd.read_csv("URLS.csv", sep=";")
    print(track_df)
    print("Position:" + str(st.session_state.position))
    new_df = pd.read_csv("URLS_SELECTED.csv", sep=";")
    print(new_df)
    row = track_df[track_df['Track Found'] == st.session_state.selected]
    row = row.head(1)
    print(row)
    new_df = pd.concat([new_df,row],ignore_index=True)
    new_df.to_csv("URLS_SELECTED.csv", sep=";", index=False)
    st.session_state.position += 1
    del st.session_state.selected


def download(title, artist, url):
    song = f"{artist} - {title}"
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': "songs/" + song + ".%(ext)s",
        'merge-output-format': 'mkv',
        'writethumbnail': False,
        'embedthumbnail': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a'
        },
        {
            'key': 'MetadataParser',
            'when': 'post_process',
            # The title and artist name are interpreted from the given song name,
            'actions': [(MetadataParserPP.Actions.INTERPRET, song, '(?P<artist>.+)\ \-\ (?P<title>.+)')]
        },
        {
            'key': 'FFmpegMetadata'
        }
        ]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

if "selected_df" not in st.session_state:
    selected_df = pd.read_csv("URLS_SELECTED.csv", sep=";", nrows=0)
    selected_df.to_csv("URLS_SELECTED.csv", sep=";", index=False)
    st.session_state.selected_df = selected_df




st.write(css, unsafe_allow_html=True)

st.image("data/Logo.png")
if "df" not in st.session_state:
    # Input field and button
    PLAYLIST_LINK = st.text_input("Enter a link")
    if st.button("Send"):
        if PLAYLIST_LINK == "":
            PLAYLIST_LINK = "https://open.spotify.com/playlist/0BoUXGxV6MGL9mF4QcbPjR?si=429b48d8acff4d1d"
        # Process the link here (e.g., print it)
        st.markdown('<br>',unsafe_allow_html=True)
        st.write(f"You entered: {PLAYLIST_LINK}")
        st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:#2B2A2A">',
                    unsafe_allow_html=True)
        # authenticate
        client_credentials_manager = SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )
        # create spotify session object
        session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        # get uri from https link
        match = re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK)
        if match:
            success = True
            playlist_uri = match.group(1)
        else:
            success = False
            st.write("Playlist not found, please check you link and try again... :)")

        if success:
            tracks = session.playlist_tracks(playlist_uri)["items"]
            names = []
            artists = []
            durations = []

            progress_text = "Connecting to Spotify API..."
            my_bar = st.progress(0, text=progress_text)
            steps = 100/len(tracks)
            counter = 0

            for track in tracks:
                time.sleep(0.01)
                counter+=steps
                if counter > 100: counter = 100
                counter = round(counter)
                my_bar.progress(counter, text=progress_text)
                name = track["track"]["name"]
                artist = ", ".join([artist["name"] for artist in track["track"]["artists"]])
                duration = track["track"]["duration_ms"]
                names.append(name)
                artists.append(artist)
                durations.append(round((duration / 1000) / 60, 2))
            dict = {'Track': names, 'Artists': artists, "Durations": durations}
            df = pd.DataFrame(dict)
            time.sleep(2)
            my_bar.empty()
            response = f"Wow, what a cool playlist! You clearly have a great taste in music :) <br><br> We found " \
                       f"{len(df)} awesome Tracks!"
            full_response= ""
            full_response_0 = ""
            message_placeholder = st.empty()
            for chunk in response.split():
                full_response_0+=chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response_0 + "❚",
                                             unsafe_allow_html=True)
            message_placeholder.markdown(full_response_0, unsafe_allow_html=True)

            st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:#2B2A2A">',
                        unsafe_allow_html=True)

            # Open YouTube ###########################################################################################

            progress_text = "Launching Scraper..."
            steps = 100 / (len(tracks))
            my_bar = st.progress(0, text=progress_text)
            counter = 0

            url = f'https://www.youtube.com'
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            urls = []
            tracks = []
            names = []
            artists = []
            durations = []
            durations_found = []
            score = []

            for index, row in df.iterrows():
                track = row["Track"]
                artist = row["Artists"]
                duration = row["Durations"]
                time.sleep(0.01)
                counter += steps
                if counter > 100:
                    counter = 100
                my_bar.progress(round(counter), text=f"{track} - {artist}")

                print("-----------------------------------------------------------------------------------")
                print(f"Currently at song {track} by {artist} ({duration}min)")
                combined = f"{track}+{artist}"
                combined = combined.replace(",", " ").replace("'", " ").replace("-", " ").replace("(", " ").replace(")"," ").replace("_", " ").replace(" ", "+")
                url = f'https://www.youtube.com/results?search_query={combined}'
                print(url)
                driver.get(url)
                path = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string'
                element = wait.until(EC.element_to_be_clickable((By.XPATH, path)))
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                counter_2 = 0
                for vid in soup.findAll(attrs={'class': 'yt-simple-endpoint style-scope ytd-video-renderer'}):
                    counter_2 = counter_2 + 1
                    if counter_2 <= 5:
                        video_link = 'https://www.youtube.com' + vid['href']
                        video_text = vid.text.replace("\n", "")
                        video_length_split = vid["aria-label"].split(" ")
                        print(video_text)
                        video_length = f"{video_length_split[-4]}.{video_length_split[-2]}"
                        tracks.append(track)
                        artists.append(artist)
                        durations.append(duration)
                        urls.append(video_link)
                        names.append(video_text)
                        durations_found.append(video_length)
                        score.append(calculate_score(track, artist, duration, video_text, video_length))

            driver.quit()
            dict = {'Track': tracks, 'Artist': artists, "Duration": durations, "Track Found": names,
                    "Duration Found": durations_found, "URL Found": urls, "Score": score}
            df = pd.DataFrame(dict)
            df.to_csv("URLS.csv", sep= ";", index=False)
            time.sleep(2)
            my_bar.empty()
            response = f"Done! We scraped all URLS, now its time for you to evaluate."
            full_response= ""
            full_response_0 = ""
            message_placeholder = st.empty()
            for chunk in response.split():
                full_response_0+=chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response_0 + "❚",
                                             unsafe_allow_html=True)
            message_placeholder.markdown(full_response_0, unsafe_allow_html=True)
            st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:#2B2A2A"><br>', unsafe_allow_html=True)

            with st.spinner():
                time.sleep(2)
            st.session_state.df = df
            st.experimental_rerun()

elif "download" not in st.session_state:
    # Selection #################################################################################################
    # Initialize new DataFrame to store selected rows
    if "selected" not in st.session_state:
        st.session_state.selected = "None"

    if "position" not in st.session_state:
        st.session_state.position = 0


    #print(selected_df)
    unique_tracks = st.session_state.df['Track'].unique()


    if st.session_state.position < len(unique_tracks):
        st.write('Please select the correct Video to download: ')
        track = unique_tracks[st.session_state.position]
        track_df = st.session_state.df[st.session_state.df['Track'] == track]
        artist = track_df['Artist'].iloc[0]

        track_options = []
        st.write(f"{track} - {artist}")
        for index, row in track_df.iterrows():
            track_options.append(f"{row['Track Found']}")

        if st.session_state.selected == "None":
            selected_option = st.radio(f"Select row for {track} - Artist: {artist}", ["None"] + track_options)
            if st.button("Send!"):
                if selected_option != "None":
                    st.session_state.selected = selected_option
                    next_step()

                    if st.session_state.position >= len(unique_tracks):
                            with st.spinner():
                                time.sleep(2)
                            st.session_state.download = "Yes"
                            st.experimental_rerun()

                    else: st.experimental_rerun()

else:
    # Display selected rows
    selected_df = pd.read_csv("URLS_SELECTED.csv", sep = ";")
    print(selected_df)


    st.write("Great! Now we will download the selected videos for you. This won't take long :)")
    progress_text = "Downloading Tracks..."
    my_bar = st.progress(0, text=progress_text)
    steps = 100 / len(selected_df)
    counter = 0

    for index, row in selected_df.iterrows():
        time.sleep(0.01)
        counter += steps
        if counter > 100:
            counter = 100
        track = row["Track"]
        artist = row["Artist"]
        url = row["URL Found"]
        my_bar.progress(round(counter), text=f"{track} - {artist}")

        download(track, artist, url)


    time.sleep(2)
    my_bar.empty()
    response = f"Done! We downloaded all songs for you. Enjoy your jam session! :)"
    full_response = ""
    full_response_0 = ""
    message_placeholder = st.empty()
    for chunk in response.split():
        full_response_0 += chunk + " "
        time.sleep(0.05)
        message_placeholder.markdown(full_response_0 + "❚",
                                     unsafe_allow_html=True)
    message_placeholder.markdown(full_response_0, unsafe_allow_html=True)



