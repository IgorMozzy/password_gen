import re
import unittest
from unittest.mock import patch

from main import generate_password, get_user_preferences_console


class TestPasswordGenerator(unittest.TestCase):

    # базовая проверка генерации паролей с переданными параметрами сразу на большой выборке
    def test_length_generate_password(self):

        L = 11
        IL = True
        ID = True
        IS = True

        passwords = [generate_password(length=L, include_letters=IL, include_digits=ID, include_symbols=IS) for
                     _ in range(1000)]
        for password in passwords:
            self.assertEqual(len(password), L)
            self.assertEqual(ID, any(char.isdigit() for char in password))
            self.assertEqual(IL, any(char.isalpha() for char in password))
            self.assertEqual(IS, bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

    # проверка корректности генерации при исключенных параметрах (без цифр, букв, символах)
    def test_params_generate_password(self):
        password = generate_password(length=20, include_letters=True, include_digits=False, include_symbols=False)
        self.assertTrue(any(char.isalpha() for char in password))
        self.assertFalse(any(char.isdigit() for char in password))
        self.assertFalse(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        password = generate_password(length=20, include_letters=False, include_digits=True, include_symbols=False)
        self.assertFalse(any(char.isalpha() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertFalse(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        password = generate_password(length=20, include_letters=False, include_digits=False, include_symbols=True)
        self.assertFalse(any(char.isalpha() for char in password))
        self.assertFalse(any(char.isdigit() for char in password))
        self.assertTrue(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        password = generate_password(length=20, include_letters=True, include_digits=True, include_symbols=False)
        self.assertTrue(any(char.isalpha() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertFalse(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        password = generate_password(length=20, include_letters=True, include_digits=False, include_symbols=True)
        self.assertTrue(any(char.isalpha() for char in password))
        self.assertFalse(any(char.isdigit() for char in password))
        self.assertTrue(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        password = generate_password(length=20, include_letters=False, include_digits=True, include_symbols=True)
        self.assertFalse(any(char.isalpha() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertTrue(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

    # ввод подменяется через unittest.mock.patch
    # проверяется корректность возвращаемых значений
    # в этом виде последовательность подтверждает, что обрабатываются ошибки некорректного ввода
    @patch('builtins.input', side_effect=['3', 'нет', '', 'нет', '1', 'да', 'да', 'нет', '5', 'да', 'да', 'нет'])
    def test_get_user_preferences(self, _):
        length, include_letters, include_digits, include_symbols = get_user_preferences_console()
        self.assertIsInstance(length, int)
        self.assertTrue(include_letters)
        self.assertTrue(include_digits)
        self.assertFalse(include_symbols)


if __name__ == '__main__':
    unittest.main()
