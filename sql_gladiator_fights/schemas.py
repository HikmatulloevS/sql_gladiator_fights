from pydantic import BaseModel
from enum import Enum


class AttackParam(str, Enum):
    head = 'head'
    chest = 'chest'
    groin = 'groin'
    feet = 'feet'


class Move(BaseModel):
    playerHit: bool
    opponentHit: bool
    playerDamageDealt: int
    opponentDamageDealt: int
    playerHealth: int
    opponentHealth: int


class Winner(BaseModel):
    winner: str
    experience: int
