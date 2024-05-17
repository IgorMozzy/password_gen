from service import PasswordGenerator, WrongParamsException


def set_user_preferences_console(password_generator):

    questions = ('Введите длину пароля: ',
                 'Обязан ли пароль содержать буквы?\nДа - любой ввод, Нет - Enter или "нет": ',
                 'Обязан ли пароль содержать цифры?\nДа - любой ввод, Нет - Enter или "нет": ',
                 'Обязан ли пароль содержать символы?\nДа - любой ввод, Нет - Enter или "нет":')

    while True:
        try:
            length = int(input(questions[0]))

            include_letters = input(questions[1]).strip().lower() not in ('', 'нет')
            include_digits = input(questions[2]).strip().lower() not in ('', 'нет')
            include_symbols = input(questions[3]).strip().lower() not in ('', 'нет')

            password_generator.set_params(length, include_letters, include_digits, include_symbols)
            break
        except (WrongParamsException, TypeError, ValueError) as e:
            print(f"Произошла ошибка: {e}")

    return length, include_letters, include_digits, include_symbols


if __name__ == "__main__":
    passgen = PasswordGenerator()
    set_user_preferences_console(passgen)

    print(passgen.generate_password())
