import unittest
from fromto import Translator


class TestTranslator(unittest.TestCase):
    def test_translate_result(self):
        translator = Translator()
        translation = translator.translate('Salom')

        self.assertEqual(translation.result(), 'Sálem')
        self.assertEqual(translation.text(), 'Salom')
        self.assertEqual(translation.from_lang(), 'uzn_Latn')
        self.assertEqual(translation.to_lang(), 'kaa')
