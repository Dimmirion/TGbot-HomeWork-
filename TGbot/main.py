import telebot
from config import TOKEN
from extensions import APIException, CryptoConverter

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Словарь с читаемыми названиями валют
CURRENCIES = {
    'евро': 'EUR (Евро)',
    'доллар': 'USD (Доллар США)',
    'рубль': 'RUB (Российский рубль)'
}


# Обработчики команд
@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = (
        "📌 *Инструкция по использованию бота:*\n\n"
        "Для конвертации валют отправьте сообщение в формате:\n"
        "`<валюта_из> <валюта_в> <количество>`\n\n"
        "_Пример:_ `евро рубль 100`\n\n"
        "Доступные команды:\n"
        "/start, /help - инструкция по использованию\n"
        "/values - список доступных валют"
    )
    bot.send_message(message.chat.id, instructions, parse_mode='Markdown')


@bot.message_handler(commands=['values'])
def send_currencies(message):
    text = "💰 *Доступные валюты:*\n\n" + "\n".join(
        f"• {name}" for name in CURRENCIES.values()
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def convert_currency(message):
    try:
        # Парсинг введённых данных
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("❌ Неверный формат запроса. Используйте: <валюта_из> <валюта_в> <количество>")

        base, quote, amount = parts
        amount = amount.replace(',', '.')  # Поддержка дробных чисел

        # Проверка и конвертация количества
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("❌ Неверное количество. Введите число.")

        # Получение результата конвертации
        result = CryptoConverter.get_price(base, quote, amount)
        bot.send_message(
            message.chat.id,
            f"💱 Результат конвертации:\n"
            f"{amount} {CURRENCIES.get(base.lower(), base)} = "
            f"{round(result, 2)} {CURRENCIES.get(quote.lower(), quote)}"
        )

    except APIException as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка:\n{str(e)}")
    except Exception as e:
        bot.send_message(message.chat.id, f"⛔ Критическая ошибка:\n{str(e)}")


if __name__ == '__main__':
    bot.polling(none_stop=True)