import os
import telebot
from telebot import types
import keyboard
from keyboard import get_command_keyboard

telegram_token = os.environ['TELEGRAM_TOKEN']
print(os.environ)
bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, reply_markup=get_command_keyboard(),
                 text='Бот для создания простых тестов.\nДля создания нового теста напишите команду /new или '
                      'отправьте ссылку на google таблцу ( пример )\n Информация оботе /about')


@bot.callback_query_handler(func=lambda c: c.data == 'about')
def process_callback_about(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Бот для создания простых тестов.\nДля создания нового теста '
                                                        'напишите команду /new или отправьте ссылку на google таблцу '
                                                        '( пример )\n Информация оботе /about')


@bot.callback_query_handler(func=lambda c: c.data == 'new')
def process_callback_new(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'тут долно быть новое чото')


@bot.callback_query_handler(func=lambda c: c.data == 'my_list')
def process_callback_my_list(callback_query: types.CallbackQuery):
   bot.answer_callback_query(callback_query.id)
   bot.send_message(callback_query.from_user.id, 'тут долно быть новое чото')


@bot.callback_query_handler(func=lambda c: c.data == 'done_list')
def process_callback_done_list(callback_query: types.CallbackQuery):
   bot.answer_callback_query(callback_query.id)
   bot.send_message(callback_query.from_user.id, 'тут долно быть новое чото')


@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, reply_markup=get_command_keyboard(),
                 text='Бот создан пользователем @black_tea_party.\nИсходный код распространяется по лицензии '
                      'GPLv3.\nРепозиторий: https://github.com/ARManakhov/sirosh-quiz-bot')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


bot.polling(none_stop=True)
