from sqlalchemy.orm import Session
from database import SessionLocal
from models import Profile
import random
import json

def get_two_profiles():
    db: Session = SessionLocal()
    profiles = db.query(Profile).all()
    sample = random.sample(profiles, 2)
    return [
        {"id": p.id, "experience": json.loads(p.experience), "education": json.loads(p.education), "image_url": p.image_url}
        for p in sample
    ]

def update_elo(rating_a, rating_b, result_a, k=32):
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    return rating_a + k * (result_a - expected_a)

def vote_on_match(winner_id: int, loser_id: int):
    db: Session = SessionLocal()
    winner = db.query(Profile).filter(Profile.id == winner_id).first()
    loser = db.query(Profile).filter(Profile.id == loser_id).first()

    winner_new = update_elo(winner.elo_rating, loser.elo_rating, 1)
    loser_new = update_elo(loser.elo_rating, winner.elo_rating, 0)

    winner.elo_rating = winner_new
    loser.elo_rating = loser_new
    db.commit()

    return {
        "winner": {"id": winner.id, "name": winner.name, "new_elo": winner.elo_rating},
        "loser": {"id": loser.id, "name": loser.name, "new_elo": loser.elo_rating},
    }
