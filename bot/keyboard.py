import telebot
from telebot import types


def get_command_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Новый тест', callback_data='/new'),
                 types.InlineKeyboardButton('Мои тесты', callback_data='/my_list'),
                 types.InlineKeyboardButton('Пройденые тесты', callback_data='/done_list'),
                 types.InlineKeyboardButton('O Боте', callback_data='/about'))
    return keyboard
