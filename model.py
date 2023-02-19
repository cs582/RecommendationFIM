from utils2 import *


class RecommendationSystem:
    def __init__(self, filedir):
        """
        Initializes a RecommendationSystem object with the given file directory.

        :param filedir: the directory where the files containing the association rules are located.
        """
        # Initialize the class with a directory containing the association rule files.
        self.filedir = filedir

        # Get the latest file in the directory.
        self.latest_file = get_latest_file(filedir)

        # Load the association rules from the latest file.
        self.rules = load_rules(filedir=filedir, filename=self.latest_file)

    def check_updates(self):
        """
        Checks if there are new updates to the association rules file and updates the rules accordingly.
        """
        # Check if there are any updates to the association rule files.
        if self.latest_file != get_latest_file(self.filedir):
            # If there are updates, update the latest file and reload the association rules.
            self.latest_file = get_latest_file(self.filedir)
            self.rules = load_rules(self.latest_file)
            print("Rules Updated!")
        else:
            print("No new updates")

    def recommendations(self, songs):
        """
        Returns a list of recommended songs based on the user's current playlist and the association rules.

        :param songs: a list of songs in the user's current playlist.
        :return: a list of recommended songs.
        """
        # Get the track and artist association rules, as well as the best songs per artist.
        track_rules = self.rules['tracks_rules']
        artist_rules = self.rules['artists_rules']
        best_per_artist = self.rules['best_per_artist']

        # Convert the list of user songs to a set for efficient comparison.
        songs = set(songs)

        # Get the set of artists for the user songs.
        artists = set([x.split(' by ')[-1] for x in songs])

        # Create an empty list to hold the recommendations.
        recommendations = []

        # Check the track association rules if the user has at least 100 songs.
        if len(songs) >= 100:
            for rule in track_rules:
                tracksA, tracksB = rule[0], rule[1]
                if tracksA.issubset(songs) and not tracksB.issubset(songs):
                    recommendations += list(tracksB)

        # Check the artist association rules if the user has between 20 and 100 songs, or if there are few recommendations.
        if len(songs) <= 100 and len(songs) > 20 or len(recommendations) <= 25:
            for rule in artist_rules:
                artistsA, artistsB = rule[0], rule[1]
                if artistsA.issubset(artists) and not artistsB.issubset(artistsB):
                    recommended_artists = artistsB
                    recommended_artists_songs = get_artists_best_songs(recommended_artists, best_per_artist)
                    recommendations += recommended_artists_songs
                    if len(recommendations) >= 100:
                        break

        # Check the best songs of the user's artists if there are less than 20 user songs, or few recommendations.
        if len(songs) <= 20 or len(recommendations) <= 10:
            benchmark_reached = False

            # Get the best songs of the user's artists.
            user_artists = get_artists_best_songs(artists, best_per_artist)
            for user_artists_songs in user_artists:
                if benchmark_reached:
                    break
                for recommended_song in user_artists_songs:
                    if benchmark_reached:
                        break
                    if not {recommended_song}.issubset(songs):
                        recommendations.append(recommended_song)
                        benchmark_reached = len(recommendations) >= 20

        return recommendations





