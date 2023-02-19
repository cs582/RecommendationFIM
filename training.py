from fpgrowth_py import fpgrowth
from utils import *

model_path = "trained_models"
data_path = "data/playlists"

dataset_file = get_latest_playlist_dataset(data_path)
data = load_data(file=f"{data_path}/{dataset_file}")
print("Data loaded")

playlists_by_tracks = collect_playlists_by_unit(data, unit="tracks")
print("Collected Playlist")
playlists_by_artists = collect_playlists_by_unit(data, unit="artists")
print("Collected Artists")

fiset_tracks, track_rules = fpgrowth(playlists_by_tracks, minSupRatio=0.008, minConf=0.95)
print(f"Model trained, discovered {len(track_rules)} rules")

fiset_artists, artist_rules = fpgrowth(playlists_by_artists, minSupRatio=0.01, minConf=0.95)
print(f"Model trained, discovered {len(artist_rules)} rules")

best_per_artist = most_popular_by_artist(data)
print("Collected most listened songs per artist!")

rules = {
    "tracks_rules": track_rules,
    "artists_rules": artist_rules,
    "best_per_artist": best_per_artist
}

save_rules(rules, model_path)