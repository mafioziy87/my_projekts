import bs4 as bs4
import requests
from datetime import date

class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА", "КОМАНДЫ","Новый_год"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        # Погода
        elif message.upper() == self._COMMANDS[1]:
            return self._get_weather()

        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()

        # Команды
        elif message.upper() == self._COMMANDS[4]:
            return f"Все команды - {self._COMMANDS}"
        # До Нового года осталось
        elif message.upper() == self._COMMANDS[5]:
            return f"До Нового года осталось - {self._get_new_year()}"
        else:
            return "Не понимаю о чем вы..."

    def _get_new_year(self):
        d=date.today()
        return d

    def _get_time(self):
        request = requests.get("https://my-calend.ru/time/novosibirsk")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.findAll("div", class_="time-item-time")))

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    def _get_weather(self, city="kansk"):
        request = requests.get("https://yandex.ru/pogoda/" + city)
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.findAll("div", class_="temp fact__temp fact__temp_size_s")))


