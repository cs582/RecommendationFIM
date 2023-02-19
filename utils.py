import os
import pickle
import numpy as np
import pandas as pd

from datetime import datetime


def get_latest_playlist_dataset(filedir):
    latest_file = sorted([x for x in os.listdir(filedir) if "playlist-sample" in x])[-1]
    return latest_file


def save_rules(rules, filedir):
    if not os.path.exists(filedir):
        os.makedirs(filedir)

    curr_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    file = f"{filedir}/fpgrowth_rules_{curr_time}.pkl"
    with open(file, "wb") as f:
        pickle.dump(rules, f)
    print(f"Model successfully saved as {file}!")


def load_data(file):
    df = pd.read_csv(file)
    return df


def collect_tracks(df):
    # Collect all tracks
    track_collection = df["track_name"] + " by " + df['artist_name']
    return track_collection.to_list()


def collect_artists(df):
    # Collect all artists
    return df['artist_name'].to_list()


def most_popular_by_artist(df):
    df['track_description'] = collect_tracks(df)
    df_temp = df[['pid', 'artist_name', 'track_description']].drop_duplicates()
    df_counts = df_temp.groupby(['artist_name', 'track_description']).count()
    df_counts.reset_index(inplace=True)

    most_listened_per_artist = []
    artists = collect_artists(df)
    for artist in artists:
        mask = (df_counts['artist_name'] == artist)
        artist_tracks = sorted(df_counts[mask]['track_description'].to_list(), reverse=True)
        top_n = min(5, len(artist_tracks))
        rule = [{artist}, set(artist_tracks[:top_n]), None]
        most_listened_per_artist.append(rule)

    return most_listened_per_artist


def collect_playlists_by_unit(df, unit="tracks"):
    units = None

    # Collect tracks
    if unit == "tracks":
        units = np.array(collect_tracks(df))
    if unit == "artists":
        units = np.array(collect_artists(df))

    # Collect all playlists
    pids = df['pid'].drop_duplicates().to_list()

    playlists = []

    for pid in pids:
        # Filter out all songs in the given playlist
        mask = (df['pid'] == pid).values
        items = list(np.unique(units[mask]))
        playlists.append(items)
    return playlists
