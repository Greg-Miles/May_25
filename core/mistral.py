from pathlib import Path
from mistralai import Mistral
from barbershop.settings import MISTRAL_MODERATION_TABLE
from .utils import MISTRAL_MODERATION_KEY
import os
from dotenv import load_dotenv
from pprint import pprint




grades = MISTRAL_MODERATION_TABLE

def is_good_review(text: str, api_key:str=MISTRAL_MODERATION_KEY, grades: dict = grades) -> bool:
    """
    Проверяет, является ли отзыв плохим, используя Mistral AI.
    :param text: Текст отзыва.
    :param api_key: Ключ API для Mistral AI.
    :param grades: Словарь с оценками для каждого класса.
    :return: True, если отзыв хороший, иначе False.
    """
    if api_key is None:
        api_key = os.getenv('MISTRAL_MODERATION_KEY')
    if not api_key:
        raise ValueError("API key is not set. Check your .env file and MISTRAL_MODERATION_KEY variable.")
    client = Mistral(api_key=api_key)

    response = client.classifiers.moderate_chat(
        model = "mistral-moderation-latest",
        inputs=[
            {
                "role": "user",
                "content": text,
            }
        ]
    )

    result = response.results[0].category_scores


    for key, value in result.items():
        if key in grades:
            if value > grades[key]:
                return False
            
    return True

if __name__ == "__main__":
    print(is_good_review("убить убить убить убить"))