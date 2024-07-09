from random import random
import uvicorn
from fastapi import FastAPI
from crud import *
from database import *
from schemas import *

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def checking():
    return "Checking"


@app.post("/api/characters")
async def create_character(name: dict, db: Session = Depends(get_db)):
    return create_char(name, db)


@app.get('/api/characters/{id}')
async def get_character(id: int, db: Session = Depends(get_db)):
    return get_char(id, db)


@app.post('/api/characters/{id}')
async def adjust_character_attributes(id: int, upgrade: dict, db: Session = Depends(get_db)):
    char = get_char(id, db)

    amount_pt = upgrade["agility"] + upgrade["stamina"] + upgrade["strength"]
    if not amount_pt <= char.availablePoints:
        raise HTTPException(status_code=404, detail='Not enough points')

    # Обновление навыков
    char.strength += upgrade["strength"]
    char.agility += upgrade["agility"]
    char.stamina += upgrade["stamina"]
    char.availablePoints -= amount_pt
    db.commit()
    db.refresh(char)
    return get_char(id, db)


@app.post('/api/lobbies')
async def create_lobby(db: Session = Depends(get_db)):
    return create_lb(db)


@app.post('/api/lobbies/{lobbyId}/join')
async def join_lobby(lobbyId: int, charId: dict, db: Session = Depends(get_db)):
    lobby = get_lobby(lobbyId, db)
    char = get_char(charId["characterId"], db)

    lobby.playerId = char.char_id

    db.commit()

    return get_lobby(lobbyId, db)


@app.post('/api/lobbies/{lobbyId}/fights')
async def start_fight(lobbyId: int, db: Session = Depends(get_db)):
    lobby = get_lobby(lobbyId, db)

    char = get_char(lobby.playerId, db)

    bot = create_bot(db, 1)

    fight = create_fight(char, bot, lobbyId, db)

    return get_fight(fight.fightId, db)


@app.post('/api/fights/{fightId}/moves')
async def make_move(fightId, attack: AttackParam, block1: AttackParam, block2: AttackParam,
                    db: Session = Depends(get_db)):
    fight = get_fight(fightId, db)

    # Получение персонажа и бота
    char = get_char(fight.fightId, db)
    bot = get_bot(fight.botId, db)

    # Ход бота
    bot_block = bot.block()
    bot_attack = bot.attack()

    ###
    playerHit = False
    opponentHit = False
    char_damage = 0
    bot_damage = 0
    ###

    # Итоги
    if not (attack in bot_block or (random() > 1 - min(0.3, bot.agility / 100))):
        char_damage = char.strength * (1.5 if random() > 1 - min(0.4, char.agility) else 1)
        bot.stamina -= char_damage
        playerHit = True
    if not (bot_attack in [block1, block2] or (random() > 1 - min(0.3, char.agility / 100))):
        bot_damage = bot.strength * (1.5 if random() > 1 - min(0.4, bot.agility) else 1)
        char.stamina -= bot_damage
        opponentHit = True

    db.commit()

    return Move(
        playerHit=playerHit,
        opponentHit=opponentHit,
        playerDamageDealt=char_damage,
        opponentDamageDealt=bot_damage,
        playerHealth=char.stamina,
        opponentHealth=bot.stamina
    )


@app.delete('/api/fights/{fightId}')
async def end_fight(fightId, db: Session = Depends(get_db)):
    fight = get_fight(fightId, db)
    char = get_char(fight.playerId, db)
    bot = get_bot(fight.botId, db)

    if char.stamina > 0 and bot.stamina > 0:
        raise HTTPException(status_code=400, detail="Fight isn't over")

    xp = 100
    winner = "player" if bot.stamina <= 0 else "bot"

    if winner == "player":
        char.xp += xp
        char.availablePoints += 5
        db.commit()
        db.refresh(char)

    db.delete(fight)
    db.commit()

    return Winner(winner=winner, experience=xp)

if __name__ == "__main__":
    uvicorn.run(app)
