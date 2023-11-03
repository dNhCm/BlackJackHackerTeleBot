import json
import math

from misc.logger import logger
from misc.project_path import get_project_path


class BlackJack:
    with open(get_project_path()+"\\blackjack\\data\\blackjack_info.json", encoding="UTF-8") as jsonfile:
        blackjack_info: dict = json.load(jsonfile)

    @classmethod
    def format_cards(cls, cards: str) -> list[int]:
        card_list: list[str] = cards.split(' ')[1:-1]
        formatted_cards: list[int | list[int]] = []
        cards_values: dict = cls.blackjack_info["cards values"]
        for card in card_list:
            card_value = cards_values.get(card)
            if not card_value:
                logger.warning(F"!!! SOMEHOW UNKNOWN CARD IN SOME CARDS FROM DB '{card}'")
            else:
                formatted_cards.append(card_value)

        if [1, 11] in formatted_cards:
            max_sum = 0
            for card in formatted_cards:
                if type(card) is list:
                    max_sum += card[1]
                else:
                    max_sum += card

            if max_sum > 21:
                delta_sum = max_sum - 21
                minus_ace_count = math.ceil(delta_sum / 11)
                minus_ace_count = max(0, min(formatted_cards.count([1, 11]), minus_ace_count))
                for _ in range(minus_ace_count):
                    formatted_cards[formatted_cards.index([1, 11])] = 1
                delta_ace = formatted_cards.count([1, 11]) - minus_ace_count
                for _ in range(delta_ace):
                    formatted_cards[formatted_cards.index([1, 11])] = 11
            else:
                for _ in range(formatted_cards.count([1, 11])):
                    formatted_cards[formatted_cards.index([1, 11])] = 11

        return formatted_cards

    @classmethod
    def get_chances(cls, in_game_cards: list[int]) -> dict[int: float]:
        chances: dict[int: float] = dict()
        for num in range(11, 0, -1):
            if num == 1 or num == 11:
                leave = (4 - in_game_cards.count(1) - in_game_cards.count(11))
            elif num == 10:
                leave = 16 - in_game_cards.count(10)
            else:
                leave = 4 - in_game_cards.count(num)

            chances[num] = leave / (52 - len(in_game_cards)) * 100

        return chances

    @classmethod
    def chances(cls, cards_in_game: str, cards: str) -> str:
        all_cards_in_game_text = ''
        own_cards = cards.split(' ')[1:-1]
        own_text = '\n'.join(own_cards)
        in_game_cards = cards_in_game.split(' ')[1:-1]
        for card in ["A", "2", "J", "3", "Q", "4", "K", "5", "6", "7", "8", "9", "10"]:
            card_count = own_cards.count(card)
            card_count += in_game_cards.count(card)
            if card_count != 0:
                all_cards_in_game_text += f"{card_count} by {card} \n"

        own_cards = cls.format_cards(cards)
        in_game_cards = own_cards + cls.format_cards(cards_in_game)

        own_text = f"{sum(own_cards)}\n" + own_text

        goal_card_value = 21 - sum(own_cards)
        chances: dict[int: float] = dict()
        for card_value, chance in cls.get_chances(in_game_cards).items():
            if card_value <= goal_card_value:
                chances[card_value] = chance

        chances_text = ""
        for card_value, chance in chances.items():
            chances_text += f"{card_value} - {round(chance, 4)}%\n"
        if 11 in chances.keys():
            chances_text += f"Defeat chance: {round(100 - sum(list(chances.values())[:-1]), 4)}%"
        else:
            chances_text += f"Defeat chance: {round(100 - sum(chances.values()), 4)}%"

        return f"""
Own:
{own_text}

All cards in game:
{all_cards_in_game_text}
Chances:
{chances_text}
"""