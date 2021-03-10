import os
from bot_operations import *
from db_operations import *
import telebot
from telebot import types

from keyboard import *

telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(telegram_token)
bot_username = bot.get_me().username


@bot.message_handler(commands=['start'])
def send_start(message):
    text = message.text
    args = text.split()[1:]
    if len(args) > 0:
        try:
            first_question = start_test_if_exist(test_id=args[0], user_id=message.from_user.id)
            bot.reply_to(message, reply_markup=get_options_keyboard(first_question), text=first_question.text)
        except NoResultFound:
            bot.reply_to(message, text='тест не найден')
        return
    bot.reply_to(message, reply_markup=get_command_keyboard(),
                 text='Бот для создания простых тестов.\nДля создания нового теста напишите команду /new или '
                      'отправьте ссылку на google таблцу ( пример )\n Информация оботе /about')


@bot.callback_query_handler(func=lambda c: c.data == 'about')
def process_callback_about(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Бот для создания простых тестов.\nДля создания нового теста '
                                                  'напишите команду /new или отправьте ссылку на google таблцу '
                                                  '( пример )\n Информация оботе /about')


@bot.callback_query_handler(func=lambda c: c.data.startswith('option'))
def process_callback_about(callback_query: types.CallbackQuery):
    args = callback_query.data.split()[1:]
    if len(args) > 0:
        option_id = args[0]
        bot.answer_callback_query(callback_query.id)
        save_answer(user_id=callback_query.from_user.id, option_id=option_id)
        next_question = get_next_question_if_exists(user_id=callback_query.from_user.id)
        if next_question is None:
            bot.send_message(callback_query.from_user.id, 'тест завершен')
        else:
            bot.send_message(callback_query.from_user.id, next_question.text,
                             reply_markup=get_options_keyboard(next_question))


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
        bot.send_message(message.from_user.id, make_test_from_spreadsheet(message.text, message.from_user.id))


bot.polling(none_stop=True)
