import requests

from .exeptions import TranslateFail
from .utils import TranslateResult


class Translator:
    """
    A class for translating text using an external translation API.

    Attributes:
        url (str): The base URL of the translation API.
    """

    def __init__(self):
        """
        Initialize a Translator object with the base URL of the translation API.
        """
        self.url = "https://api.from-to.uz/api/v1/translate"

    def translate(self, text: str, from_lang: str = "uzn_Latn", to_lang: str = "kaa"):
        """
        Translate text from one language to another using the translation API.

        Args:
            text (str): The text to be translated.
            from_lang (str, optional): The code representing the original language of the text. Defaults to "uzn_Latn".
            to_lang (str, optional): The code representing the target language for translation. Defaults to "kaa".

        Returns:
            TranslateResult: An object representing the translation result.

        Raises:
            TranslateFail: If there is an issue with the translation request.
        """
        data = {
            "body": {
                "lang_from": from_lang,
                "lang_to": to_lang,
                "text": text,
            }
        }

        try:
            response = requests.post(self.url, json=data)
            response.raise_for_status()
            result = TranslateResult(text=text, result=response.json(), from_lang=from_lang, to_lang=to_lang)

            return result

        except Exception as e:
            raise TranslateFail(text=text, from_lang=from_lang, to_lang=to_lang)
