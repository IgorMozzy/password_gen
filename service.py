import string
import secrets


class WrongParamsException(Exception):
    """Any inappropriate parameters """
    pass


class PasswordGenerator:
    def __init__(self, length: int = 12,
                 include_letters: bool = True,
                 include_digits: bool = True,
                 include_symbols: bool = True) -> None:
        # Добавил параметры по умолчанию None чтобы убрать предупреждение
        # Instance attribute _include_letters defined outside __init__
        # Но вообще предпочел бы этого не делать...
        self._length = None
        self._include_letters = None
        self._include_digits = None
        self._include_symbols = None

        self.set_params(length, include_letters, include_digits, include_symbols)

    def set_params(self, length: int,
                   include_letters: bool,
                   include_digits: bool,
                   include_symbols: bool) -> None:
        params = length, include_letters, include_digits, include_symbols
        defaults = int(), bool(), bool(), bool()
        for param, default in zip(params, defaults):
            if not isinstance(param, type(default)):
                raise TypeError('Wrong data type')
        bool_params = (include_letters, include_digits, include_symbols)
        if not any(bool_params):
            raise WrongParamsException('At least one option must be selected')
        if length < sum(bool_params):
            raise WrongParamsException(f'Minimum length for selected options: {sum(bool_params)}')
        else:
            self._length = length
            self._include_letters = include_letters
            self._include_digits = include_digits
            self._include_symbols = include_symbols

    def get_source_string(self) -> str:

        characters = ''
        if self._include_letters:
            characters += string.ascii_letters
        if self._include_digits:
            characters += string.digits
        if self._include_symbols:
            characters += string.punctuation

        return characters

    def is_valid(self, password: str) -> bool:
        # Проверка соответствия пароля условиям по следующей логике:
        # "флаги" изначально в False, поэтому справа от or проверяется соответствие типа символа с правилом.
        # Если данный тип символов не используется, все выражение становится истинным на первом символе
        is_letters = is_letters_up = is_digits = is_symbols = False
        for char in password:
            is_letters = is_letters or self._include_letters is char.isalpha()
            is_letters_up = is_letters_up or self._include_letters is char.isupper()
            is_digits = is_digits or self._include_digits is char.isdigit()
            is_symbols = is_symbols or self._include_symbols is (char in r"[!\"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]")
            if is_letters and is_letters_up and is_digits and is_symbols:
                # досрочный выход из цикла, если пароль уже соответствует критериям
                return True
        return False

    def generate_password(self) -> str:
        source_str = self.get_source_string()
        for _ in range(100):
            password = ''.join(secrets.choice(source_str) for _ in range(self._length))
            if self.is_valid(password):
                return password
        else:
            return 'Generation error. Repeat or message Pavel Durov'
