import os
import telebot

telegram_token = os.environ['TELEGRAM_TOKEN']
print(os.environ)
bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Бот для создания простых тестов.\nДля создания нового теста напишите команду /new, '
                          'или отправьте ссылку на google таблцу ( пример )\n'
                          'Информация оботе /about')


@bot.message_handler(commands=['about'])
def send_welcome(message):
    bot.reply_to(message, 'Бот создан пользователем @green_tea_party.\nИсходный код распространяется по лицензии '
                          'GPLv3.\n Репозиторий: https://github.com/ARManakhov/sirosh-quiz-bot')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


bot.polling(none_stop=True)
