# FastAPI entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from dotenv import load_dotenv
from databases import Database
import os
import random

from models import profiles, metadata, engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()
database = Database(DATABASE_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/match")
async def get_match():
    query = select(profiles).order_by(profiles.c.elo.desc()).limit(50)
    rows = await database.fetch_all(query)
    match = random.sample(rows, 2)
    return match

@app.post("/vote")
async def vote(winner_id: int, loser_id: int):
    winner = await database.fetch_one(select(profiles).where(profiles.c.id == winner_id))
    loser = await database.fetch_one(select(profiles).where(profiles.c.id == loser_id))

    def calculate_elo(winner_elo, loser_elo, k=32):
        expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        return winner_elo + k * (1 - expected_win)

    new_winner_elo = calculate_elo(winner["elo"], loser["elo"])
    new_loser_elo = calculate_elo(loser["elo"], winner["elo"], k=32)

    await database.execute(profiles.update().where(profiles.c.id == winner_id).values(elo=new_winner_elo))
    await database.execute(profiles.update().where(profiles.c.id == loser_id).values(elo=new_loser_elo))

    return {"status": "ok"}
