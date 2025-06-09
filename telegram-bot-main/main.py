from dotenv import load_dotenv
from management import init_db, add_user, get_stats, update_stats
import os
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from photo_cat import get_photo_cat


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Создание gamedb.sql
init_db()

# Игровые значения.
number_user = 0
game_number = None
attempt = 0


# Команда старт бота.
@bot.message_handler(commands=['start'])
def start_bot(message):
    add_user(message.from_user.id, message.from_user.username)
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton(text='Начать', callback_data="begin")
    button_stats = InlineKeyboardButton(text='Статистика', callback_data="stats")
    markup.add(button_1, button_stats)
    bot.send_message(
        message.chat.id,
        text=f'👋 Привет {message.from_user.username}, '
             f'хочешь поиграть угадай число?'
             '\n🤔 Если ты готов жми на кнопку "Начать".'
             '\nПравила игры будут по команде /help.',
        reply_markup=markup
    )


# Команда помощь, показывает правила.
@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.send_message(
        message.chat.id,
        text="Правила игры очень просты. Бот загадал число от 1 до 100, "
             "надо будет вводить числа которые загадал бот😁. "
             "НО у тебя будет только 6 попыток, также он будет тебе "
             "подсказывать больше или меньше. Если ты "
             "готов ... и хорошей тебе игры."
    )


# Команда для регистрации числа пользователя.
@bot.callback_query_handler(func=lambda call:True)
def user_number_registration(call):
    global game_number
    global attempt
    game_number = random.randint(1, 100)
    attempt = 6

    if call.data == "stats":
        user_id = call.from_user.id
        games, winning = get_stats(user_id)
        bot.send_message(
            call.message.chat.id,
            text=f"📊 Твоя статистика: {call.message.from_user.username}"
                 f"\n🎮 Игр сыграно: {games}"
                 f"\n🏆 Побед: {winning}"
        )
        return

    if call.data == "begin":
        bot.send_message(
            call.message.chat.id,
            text="Напиши число от 1 до 100."
        )
        bot.register_next_step_handler(call.message, game_logic)


# Перезапуск игры.
def send_play_again_button(chat_id):
    markup = InlineKeyboardMarkup()
    button_2 = InlineKeyboardButton(
        text="🎲 Сыграть ещё раз 🎲",
        callback_data="begin"
    )
    markup.add(button_2)
    bot.send_message(
        chat_id,
        text="Хочешь сыграть ещё раз?",
        reply_markup=markup
    )


# Игровая логика.
def game_logic(message):
    global number_user
    global game_number
    global attempt
    print(f'Загаданное число: {game_number}')
    print(f"осталось попыток {attempt}")

    try:
        number_user = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, text="🎲 Я жду только число.")
        bot.register_next_step_handler(message, game_logic)
        return

    if attempt > 0:
        if number_user == game_number:
            chat_id = message.chat.id
            bot.send_photo(chat_id, get_photo_cat())
            bot.send_message(
                message.chat.id,
                text=f"🎉 Молодец ты угадал число {game_number}. Держи котика🐈"
            )
            update_stats(message.from_user.id, winning=True)
            send_play_again_button(message.chat.id)

        elif number_user > game_number:
            attempt -= 1
            bot.send_message(
                message.chat.id,
                text=f"Меньше👇.\nОсталось попыток: {attempt}"
            )
            bot.register_next_step_handler(message, game_logic)

        elif number_user < game_number:
            attempt -= 1
            bot.send_message(
                message.chat.id,
                text=f"Больше👆.\nОсталось попыток: {attempt}"
            )
            bot.register_next_step_handler(message, game_logic)

    if attempt <= 0:
        bot.send_message(message.chat.id, text='❌ Увы попытки закончились.')
        update_stats(message.from_user.id, winning=False)
        send_play_again_button(message.chat.id)
        return

def main():
    bot.polling(non_stop=True)


if __name__ == "__main__":
    print("БОТ ЗАПУЩЕН...")
    main()
    print("БОТ ЗАВЕРШИЛ СЕАНС.")
