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
user_data = {}


@bot.message_handler(commands=['start'])
def start_bot(message):
    """Команда старта бота."""
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


@bot.message_handler(commands=['help'])
def help_bot(message):
    """Команда помощь, показывает правила."""
    bot.send_message(
        message.chat.id,
        text="Правила игры очень просты. Бот загадал число от 1 до 100, "
             "надо будет вводить числа которые загадал бот😁. "
             "НО у тебя будет только 6 попыток, также он будет тебе "
             "подсказывать больше или меньше. Если ты "
             "готов ... и хорошей тебе игры."
    )


@bot.callback_query_handler(func=lambda call:True)
def user_number_registration(call):
    """Команда для регистрации числа пользователя."""
    if call.data == "stats":
        user_id = call.from_user.id
        games, winning = get_stats(user_id)
        bot.send_message(
            call.message.chat.id,
            text=f"📊 Твоя статистика: {call.message.from_user.username}"
                 f"\n🎮 Игр сыграно: {games}"
                 f"\n🏆 Побед: {winning}"
        )
        send_play_again_button(call.message.chat.id)

    if call.data == "begin":
        user_id = call.from_user.id
        user_data[user_id] = {
            "number": random.randint(1, 100),
            "attempt": 6
        }
        bot.send_message(
            call.message.chat.id,
            text="Напиши число от 1 до 100."
        )
        bot.register_next_step_handler(call.message, game_logic)


@bot.message_handler()
def send_play_again_button(chat_id):
    """Перезапуск игры."""
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


def game_logic(message):
    """Игровая логика."""
    user_id = message.from_user.id

    if user_id not in user_data:
        bot.send_message(message.chat.id, text="❗ Начни игру командой /start или нажми кнопку.")

    try:
        number_user = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, text="🎲 Я жду только число.")
        bot.register_next_step_handler(message, game_logic)
        return

    target_number = user_data[user_id]["number"]
    attempt = user_data[user_id]["attempt"]

    if attempt > 0:
        if number_user == target_number:
            bot.send_photo(message.chat.id, get_photo_cat())
            bot.send_message(
                message.chat.id,
                text=f"🎉 Молодец, ты угадал число: {target_number}"
                     f"\n🐈 Держи котика."
            )
            update_stats(user_id, winning=True)
            user_data.pop(user_id)
            send_play_again_button(message.chat.id)
            return

        else:
            attempt -= 1
            user_data[user_id]["attempt"] = attempt
            hint = "Меньше👇" if number_user > target_number else "Больше👆"
            bot.send_message(
                message.chat.id,
                text=f"{hint}\nОсталось попыток: {attempt}"
            )

            if attempt > 0:
                bot.register_next_step_handler(message, game_logic)
            else:
                bot.send_message(message.chat.id, "❌ Увы, попытки закончились.")
                update_stats(user_id, winning=False)
                user_data.pop(user_id)
                send_play_again_button(message.chat.id)


def main():
    bot.polling(non_stop=True)


if __name__ == "__main__":
    print("БОТ ЗАПУЩЕН...")
    main()
    print("БОТ ЗАВЕРШИЛ СЕАНС.")

# Переделать систему показа статистики (Показывать рейтинг всех пользователей).
# Убрать сообщение если не осталось попыток для чисел.
