import string  # символьные константы
import secrets  # генерация безопасных случайных чисел и строк


def generate_password(length=12, include_letters=True, include_digits=True, include_symbols=True):
    while True:

        if length < sum([include_letters, include_digits, include_symbols]):
            raise ValueError

        characters = ''
        if include_letters:
            characters += string.ascii_letters
        if include_digits:
            characters += string.digits
        if include_symbols:
            characters += string.punctuation

        password = ''.join(secrets.choice(characters) for _ in range(length))

        # Проверка соответствия пароля условиям по следующей логике:
        # "флаги" изначально в False, поэтому справа от or проверяется соответствие типа символа с правилом.
        # Если данный тип символов не используется, все выражение становится истинным на первом символе
        def check_cond():
            letters = letters_up = digits = symbols = False
            for char in password:
                letters = letters or include_letters is char.isalpha()
                letters_up = letters_up or include_letters is char.isupper()
                digits = digits or include_digits is char.isdigit()
                symbols = symbols or include_symbols is (char in r"[!\"#$%&'()*+,-./:;<=>?@[\\\]^_`{|}~]")
                if letters and letters_up and digits and symbols:
                    return True
                    # досрочный выход из цикла, если пароль уже соответствует критериям
            return False

        # бесконечная генерация подходящего пароля
        if not check_cond():
            continue

        return password


# функция для пользовательского вода в консоли
# в планах:
# было бы неплохо в целом переделать всю логику на более очевидную
# и т.к. здесь обрабатываются ошибки, просто возвращать ответы с исключениями, а сам консольный ввод вынести олтдельно
def get_user_preferences_console():
    params = {'Введите длину пароля: ': int(),
              'Обязан ли пароль содержать буквы?\nДа - любой ввод, Нет - Enter или "нет": ': bool(),
              'Обязан ли пароль содержать цифры?\nДа - любой ввод, Нет - Enter или "нет": ': bool(),
              'Обязан ли пароль содержать символы?\nДа - любой ввод, Нет - Enter или "нет": ': bool()}
    while True:
        try:
            # введенные значения приводятся к значению соответствующего типа из словаря, чье место и занимают
            params = {k: type(v)(input(k).lower().split('нет')[0]) for k, v in params.items()}
            if not any(list(params.values())[1:]):
                print('Хотя бы один из параметров составления должен быть истинным'
                      ' (буквы, цифры, символы). Повторите ввод.')
                continue
            if list(params.values())[1:].count(True) > list(params.values())[0]:
                print(f'Для выбранных параметров минимальная длина: {list(params.values())[1:].count(True)}')
                continue
        except ValueError:
            print('Некорректные данные, повторите ввод: ')
            continue

        return params.values()


def main():
    length, include_letters, include_digits, include_symbols = get_user_preferences_console()
    password = generate_password(length, include_letters, include_digits, include_symbols)
    print("Сгенерированный пароль:", password)


if __name__ == "__main__":
    main()
