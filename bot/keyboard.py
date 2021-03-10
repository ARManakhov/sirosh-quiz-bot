from telebot import types


def get_command_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Новый тест', callback_data='new'),
                 types.InlineKeyboardButton('Мои тесты', callback_data='my_list'),
                 types.InlineKeyboardButton('Пройденые тесты', callback_data='done_list'),
                 types.InlineKeyboardButton('O Боте', callback_data='about'))
    return keyboard


def get_options_keyboard(question):
    keyboard = types.InlineKeyboardMarkup()
    for o in question.options:
        keyboard.add(types.InlineKeyboardButton(o.text, callback_data=("option" + str(o.id))))
    return keyboard
