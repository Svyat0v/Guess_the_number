import random


attempt = 7


def game_logic(game_number):
    global attempt
    print(f"Загаданное случайное число: {game_number}")

    while attempt > 0:

        number_user = int(input("Введи число: "))

        if number_user == game_number:
            break

        elif number_user > game_number:
            attempt -= 1
            print(f"Меньше")
            continue

        elif number_user < game_number:
            attempt -= 1
            print(f"Больше")
            continue

    if number_user == game_number:
        print(f"Молодец ты угадал число {game_number}")

    elif attempt == 0:
        print(f"Увы попытки закончились.")

    else:
        print(f"Что то пошло не так.")


if __name__ == "__main__":
    number_game = random.randint(1, 100)
    print('Игра началась.')
    game_logic(number_game)
