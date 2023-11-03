
from sqlite3 import Row, OperationalError
from typing import Optional

import aiosqlite as asql
from aiosqlite import Connection

from misc.logger import logger


class BlackJackDatabase:
    _db: Connection = None
    name = "./tgbot/models/blackjack.db"

    @classmethod
    async def get_conn(cls) -> Optional[Connection]:
        if not cls._db:
            cls._db = await asql.connect(cls.name)
            if cls._db:
                logger.info("BlackJackDatabase was connected successfully!")
            else:
                logger.warning("!!! BlackJackDatabase WAS NOT CONNECTED !!!")
        return cls._db

    @classmethod
    async def init_user_tables_table(cls):
        conn = await cls.get_conn()
        c = await conn.cursor()

        await c.execute("""CREATE TABLE IF NOT EXISTS usersTable (
                user_id                 INTEGER,
                table_message_id        INTEGER,
                cards_in_game           VARCHAR(255),
                cards                   CHARACTER(20)
            )""")

        await conn.commit()

    @classmethod
    async def insert_user_table(cls, user_id: int) -> bool:
        conn = await cls.get_conn()
        c = await conn.cursor()

        if cls.check_exists_user_table(user_id):
            return False

        await c.execute(f"""INSERT INTO usersTable (user_id, table_message_id, cards_in_game, cards)
        VALUES ({user_id}, 0, '0 ', '0 ')""")

        await conn.commit()
        return True

    @classmethod
    async def add_cards(cls, user_id: int, cards_in_game: str = None, cards: str = None) -> bool:
        conn = await cls.get_conn()
        c = await conn.cursor()

        if not await cls.check_exists_user_table(user_id):
            return False

        await c.execute(f"""SELECT cards_in_game, cards FROM usersTable
        WHERE user_id = {user_id}""")

        record = await c.fetchone()
        cards_in_game_db = str(record[0])
        cards_db = str(record[1])

        if cards_in_game:
            cards_in_game = cards_in_game.split(' ')
            for card_in_game in cards_in_game:
                cards_in_game_db += f"{card_in_game} "
        if cards:
            cards = cards.split(' ')
            for card in cards:
                cards_db += f"{card} "

        await c.execute(f"""UPDATE usersTable
            SET cards_in_game = '{cards_in_game_db}',
                cards = '{cards_db}'
            WHERE user_id = {user_id}
        """)

        await conn.commit()
        return True

    @classmethod
    async def del_cards(cls, user_id: int, cards_in_game: str = None, cards: str = None) -> Optional[list[str]]:
        conn = await cls.get_conn()
        c = await conn.cursor()

        if not await cls.check_exists_user_table(user_id=user_id):
            return None

        await c.execute(f"""SELECT cards_in_game, cards FROM usersTable
                WHERE user_id = {user_id}""")

        record = await c.fetchone()
        cards_in_game_db = str(record[0]).split(' ')[:-1]
        cards_db = str(record[1]).split(' ')[:-1]

        deleted_cards: list[str] = []
        if cards_in_game:
            cards_in_game = cards_in_game.split(' ')
            for card_in_game in cards_in_game:
                if card_in_game in cards_in_game_db:
                    cards_in_game_db.remove(card_in_game)
                    deleted_cards.append(card_in_game)
        if cards:
            cards = cards.split(' ')
            for card in cards:
                if card in cards_db:
                    cards_db.remove(card)
                    deleted_cards.append(card)

        cards_in_game_db = " ".join(cards_in_game_db)
        cards_db = " ".join(cards_db)
        await c.execute(f"""UPDATE usersTable
                    SET cards_in_game = '{cards_in_game_db}',
                        cards = '{cards_db}'
                    WHERE user_id = {user_id}
                """)

        await conn.commit()
        return deleted_cards

    @classmethod
    async def check_exists_user_table(cls, user_id: int) -> bool:
        conn = await cls.get_conn()
        c = await conn.cursor()

        await c.execute(f"""SELECT user_id FROM usersTable
                WHERE user_id = {user_id}""")

        record: Row = await c.fetchall()
        if len(record) > 0:
            return True
        return False

    @classmethod
    async def new_user_table(cls, user_id: int, message_id: int) -> bool:
        conn = await cls.get_conn()
        c = await conn.cursor()

        if not await cls.check_exists_user_table(user_id):
            return False

        await c.execute(f"""UPDATE usersTable
                SET table_message_id = {message_id},
                    cards_in_game = '0 ',
                    cards = '0 '
                WHERE user_id = {user_id}
            """)

        await conn.commit()
        return True

    @classmethod
    async def get_user_table_data(cls, user_id: int) -> Optional[dict[int | list[dict[str]]]]:
        conn = await cls.get_conn()
        c = await conn.cursor()

        if not await cls.check_exists_user_table(user_id):
            return None

        await c.execute(f"""SELECT table_message_id, cards_in_game, cards FROM usersTable
        WHERE user_id = {user_id}""")

        result = await c.fetchone()
        table_message_id = int(result[0])
        cards_in_game = str(result[1])
        cards = str(result[2])

        return {
            "user_id": user_id,
            "table_message_id": table_message_id,
            "cards_in_game": cards_in_game,
            "cards": cards
        }


async def main():
    await BlackJackDatabase.init_user_tables_table()
