from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from main import get_db
from models import *


def create_char(name: dict, db):
    char = Character(name=name["name"])
    db.add(char)
    db.commit()
    db.refresh(char)
    return char


def create_lb(db):
    lb = Lobby()
    db.add(lb)
    db.commit()
    db.refresh(lb)
    return lb


def create_bot(db, level: int = 1):
    bot = Bot(level=level)
    bot.stamina = bot.return_random()
    bot.strength = bot.return_random()
    bot.agility = bot.return_random()

    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


def create_fight(char: Character, bot: Bot, lobbyId: Lobby, db):
    fight = Fight(player_turn=True, playerId=char.char_id, botId=bot.bot_id, lobbyId=lobbyId)

    db.add(fight)
    db.commit()
    db.refresh(fight)
    return fight


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


def del_fight(id: int, db):
    pass
