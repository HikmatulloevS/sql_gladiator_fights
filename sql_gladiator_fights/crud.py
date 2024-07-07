from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from main import get_db
from models import *


def get_char(id: int, db):
    char = db.query(Character).filter_by(char_id=id).first()
    if not char:
        raise HTTPException(status_code=400, detail="Can't find character")
    return char


def get_lobby(id: int, db):
    lb = db.query(Lobby).filter_by(lobbyId=id).first()
    if not lb:
        raise HTTPException(status_code=400, detail="Can't find lobby")
    return lb


def get_bot(id: int, db):
    bot = db.query(Bot).filter_by(bot_id=id).first()
    if not bot:
        raise HTTPException(status_code=400, detail="Can't find bot")
    return bot


def get_fight(id: int, db):
    f = db.query(Fight).filter_by(fightId=id).first()
    if not f:
        raise HTTPException(status_code=400, detail="Can't find fight")
    return f
