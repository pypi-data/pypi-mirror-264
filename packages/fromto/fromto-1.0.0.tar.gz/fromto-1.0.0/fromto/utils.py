class TranslateResult:
    """
    Represents the result of a translation operation.

    Attributes:
        _text (str): The original text that was translated.
        _result (str): The translated text.
        _from_lang (str): The language code representing the original language of the text.
        _to_lang (str): The language code representing the target language for translation.
    """

    def __init__(self, text: str, result: dict, from_lang: str, to_lang: str):
        """
        Initialize TranslateResult with the provided attributes.

        Args:
            text (str): The original text that was translated.
            result (dict): The translated text.
            from_lang (str): The language code representing the original language of the text.
            to_lang (str): The language code representing the target language for translation.
        """
        self._text = text
        self._result = result['result']
        self._from_lang = from_lang
        self._to_lang = to_lang

    def json(self):
        """
        Return a dictionary representation of the translation result.

        Returns:
            dict: A dictionary containing the original text, translated text, original language, and target language.
        """
        return {
            "text": self._text,
            "result": self._result,
            "from_lang": self._from_lang,
            "to_lang": self._to_lang
        }

    def text(self):
        """
        Get the original text.

        Returns:
            str: The original text that was translated.
        """
        return self._text

    def result(self):
        """
        Get the translated text.

        Returns:
            str: The translated text.
        """
        return self._result

    def from_lang(self):
        """
        Get the original language.

        Returns:
            str: The language code representing the original language of the text.
        """
        return self._from_lang

    def to_lang(self):
        """
        Get the target language.

        Returns:
            str: The language code representing the target language for translation.
        """
        return self._to_lang

    def __str__(self):
        """
        Return a string representation of the translated text.

        Returns:
            str: A string containing information about the translation result.
        """
        return f"text: \"{self._text}\", result: \"{self._result}\", from_lang: \"{self._from_lang}\", to_lang: \"{self._to_lang}\""
