from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base

from random import sample, choice, randint


class Character(Base):
    __tablename__ = "character"

    char_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    strength: Mapped[int] = mapped_column(Integer, default=10)
    agility: Mapped[int] = mapped_column(Integer, default=10)
    stamina: Mapped[int] = mapped_column(Integer, default=10)
    level: Mapped[int] = mapped_column(Integer, default=1)
    availablePoints: Mapped[int] = mapped_column(Integer, default=10)
    xp: Mapped[int] = mapped_column(Integer, default=0)


    # player_id = relationship("Fight", back_populates="char_relation")


#
#
class Bot(Base):
    __tablename__ = "bot"

    bot_id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[int] = mapped_column(Integer, default=1)
    strength: Mapped[int] = mapped_column(Integer, default=0)
    agility: Mapped[int] = mapped_column(Integer, default=0)
    stamina: Mapped[int] = mapped_column(Integer, default=0)

    def return_random(self):
        return randint(self.level * 5, self.level * 8)

    # b_id = relationship("Fight", back_populates="bot_relation")

    @staticmethod
    def attack():
        return choice(['head', 'chest', 'groin', 'feet'])

    @staticmethod
    def block():
        return sample(['head', 'chest', 'groin', 'feet'], 2)


class Lobby(Base):
    __tablename__ = "lobby"

    lobbyId: Mapped[int] = mapped_column(primary_key=True)
    playerId: Mapped[int] = mapped_column(Integer, default=0)


#
# lobby_id = relationship("Fight", back_populates="lobby_relation")


class Fight(Base):
    __tablename__ = "fight"

    fightId: Mapped[int] = mapped_column(primary_key=True)
    player_turn: Mapped[bool] = mapped_column(Boolean, default=False)
    playerId: Mapped[int] = mapped_column(Integer, default=0)
    botId: Mapped[int] = mapped_column(Integer, default=0)
    lobbyId: Mapped[int] = mapped_column(Integer, default=0)

    # char_relation = relationship("Character", back_populates="player_id")
    # bot_relation = relationship("Bot", back_populates="b_id")
    # lobby_relation = relationship("Lobby", back_populates="lobby_id")
