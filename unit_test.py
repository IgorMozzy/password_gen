import re
import unittest
from unittest.mock import patch

from console_out import set_user_preferences_console
from service import PasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    def test_length_generate_password(self):
        # Базовая проверка генерации паролей с переданными параметрами сразу на большой выборке

        L = 11
        IL = True
        ID = True
        IS = True

        passgen = PasswordGenerator()
        passgen.set_params(L, IL, ID, IS)

        passwords = [passgen.generate_password() for _ in range(1000)]
        for password in passwords:
            self.assertEqual(len(password), L)
            self.assertEqual(ID, any(char.isdigit() for char in password))
            self.assertEqual(IL, any(char.isalpha() for char in password))
            self.assertEqual(IS, bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

    def test_params_generate_password(self):
        # проверка корректности генерации при исключенных параметрах (без цифр, букв, символах)

        passgen = PasswordGenerator()
        passgen.set_params(length=20, include_letters=True, include_digits=False, include_symbols=False)

        password = passgen.generate_password()

        self.assertTrue(any(char.isalpha() for char in password))
        self.assertFalse(any(char.isdigit() for char in password))
        self.assertFalse(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        passgen.set_params(length=20, include_letters=False, include_digits=True, include_symbols=False)
        password = passgen.generate_password()
        self.assertFalse(any(char.isalpha() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertFalse(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        passgen.set_params(length=20, include_letters=False, include_digits=False, include_symbols=True)
        password = passgen.generate_password()
        self.assertFalse(any(char.isalpha() for char in password))
        self.assertFalse(any(char.isdigit() for char in password))
        self.assertTrue(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        passgen.set_params(length=20, include_letters=True, include_digits=True, include_symbols=False)
        password = passgen.generate_password()
        self.assertTrue(any(char.isalpha() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertFalse(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        passgen.set_params(length=20, include_letters=True, include_digits=False, include_symbols=True)
        password = passgen.generate_password()
        self.assertTrue(any(char.isalpha() for char in password))
        self.assertFalse(any(char.isdigit() for char in password))
        self.assertTrue(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

        passgen.set_params(length=20, include_letters=False, include_digits=True, include_symbols=True)
        password = passgen.generate_password()
        self.assertFalse(any(char.isalpha() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertTrue(bool(re.search(r'[!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~]', password)))

    @patch('builtins.input', side_effect=['3', 'нет', '', 'нет', '1', 'да', 'да', 'нет', '5', 'да', 'да', 'нет'])
    def test_get_user_preferences(self, _):
        # ввод подменяется через unittest.mock.patch
        # проверяется корректность возвращаемых значений
        # в этом виде последовательность подтверждает, что обрабатываются ошибки некорректного ввода
        passgen = PasswordGenerator()
        length, include_letters, include_digits, include_symbols = set_user_preferences_console(passgen)
        self.assertIsInstance(length, int)
        self.assertTrue(include_letters)
        self.assertTrue(include_digits)
        self.assertFalse(include_symbols)


if __name__ == '__main__':
    unittest.main()
