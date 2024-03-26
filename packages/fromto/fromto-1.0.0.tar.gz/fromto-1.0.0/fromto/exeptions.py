class TranslateFail(Exception):
    """
    Exception raised when a translation request fails.

    Attributes:
        text (str): The text that was attempted to be translated.
        from_lang (str): The language code representing the original language of the text.
        to_lang (str): The language code representing the target language for translation.
        message (str): A message describing the failure. Defaults to "There was a problem sending the request.".
    """

    def __init__(self, text: str, from_lang: str, to_lang: str, message: str = "There was a problem sending the request."):
        """
        Initialize TranslateFail with the provided attributes.

        Args:
            text (str): The text that was attempted to be translated.
            from_lang (str): The language code representing the original language of the text.
            to_lang (str): The language code representing the target language for translation.
            message (str, optional): A message describing the failure. Defaults to "There was a problem sending the request.".
        """
        self.text = text
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        """
        Return a string representation of the exception.

        Returns:
            str: A string containing information about the translation failure.
        """
        return f"from: \"{self.from_lang}\", to: \"{self.to_lang}\", text: \"{self.text}\", message: {self.message}"
