import numpy as np
from utils import *
from model import RecommendationSystem

data = load_data(file="data//songs.csv")
print("Data loaded")

test_songs = np.random.choice(collect_tracks(data), size=int(np.random.randint(50)))

print(f"Testing with {len(test_songs)} songs.")

models_dir = "trained_models"
rs = RecommendationSystem(models_dir)
rs.check_updates()
recommendations = rs.recommendations(test_songs)

print(f"Gotten {len(recommendations)} recommendations.")