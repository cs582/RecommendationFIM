import os
import pickle


def load_rules(filedir, filename):
    file = f"{filedir}/{filename}"
    with open(file, "rb") as f:
        rules = pickle.load(f)
    return rules


def get_latest_file(filedir):
    latest_file = sorted([x for x in os.listdir(filedir) if "fpgrowth_rules" in x])[-1]
    return latest_file


def get_artists_best_songs(artists, best_per_artist):

    songs = []

    for rule in best_per_artist:
        curr_artist, curr_artist_best = rule[0], rule[1]
        if curr_artist.issubset(artists):
            songs.append(list(curr_artist_best))

    return songs
