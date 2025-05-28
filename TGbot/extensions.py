import requests
import json


class APIException(Exception):
    """Пользовательское исключение для ошибок API"""
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        """
        Конвертирует валюту через API Cryptocompare
        :param base: базовая валюта (из которой конвертируем)
        :param quote: котируемая валюта (в которую конвертируем)
        :param amount: количество конвертируемой валюты
        :return: итоговая сумма после конвертации
        """
        # Словарь соответствия русских названий к кодам валют
        currencies = {
            'евро': 'EUR',
            'доллар': 'USD',
            'рубль': 'RUB'
        }

        # Приведение введённых названий к нижнему регистру
        base = base.lower()
        quote = quote.lower()

        # Проверка наличия валют в словаре
        if base not in currencies:
            raise APIException(f"Валюта {base} не найдена. Доступные валюты: /values")
        if quote not in currencies:
            raise APIException(f"Валюта {quote} не найдена. Доступные валюты: /values")

        # Запрос к API
        url = f"https://min-api.cryptocompare.com/data/price?fsym={currencies[base]}&tsyms={currencies[quote]}"
        response = requests.get(url)
        data = json.loads(response.text)

        # Обработка ошибок API
        if response.status_code != 200:
            raise APIException("Ошибка сервера. Попробуйте позже.")
        if 'Error' in data:
            raise APIException(data['Error'])

        # Получение курса и расчёт результата
        rate = data.get(currencies[quote])
        if rate is None:
            raise APIException(f"Невозможно получить курс для пары {base}/{quote}")

        return rate * amount