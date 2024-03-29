import urllib.request
from typing import List, Dict

import requests


class TelegramConnectorException(ValueError):
    pass


class TelegramConnector:
    url = "https://api.telegram.org/bot"

    def __init__(self, config):
        try:
            self.bot_token = '6722982894:AAGdHkbU5BoPorK7NFlbIBiJKbWJEZ0YxnI'  # токен бота
            self.chat_id = int('5337729489')  # id чата
        except KeyError:
            raise TelegramConnectorException("bot_token и chat_id обязательные параметры конфига")
        except ValueError:
            raise TelegramConnectorException("ошибка заполнения chat_id")

        self._offset = 1

    def send_message(self, msg):
        self._send_request(
            url=f"{self.url}{self.bot_token}/sendMessage?chat_id={self.chat_id}",
            json={
                'text': msg,
                'disable_web_page_preview': True
            }
        )

    def send_pic(self, img_byte_arr):
        files = {'document': ('1.png', img_byte_arr)}
        data = {'parse_mode': 'HTML'}
        self._send_request(
            url=f"{self.url}{self.bot_token}/sendDocument?chat_id={self.chat_id}",
            data=data,
            files=files,
            stream=True
        )

    def set_commands(self, commands: List[Dict]):
        self._send_request(
            url=f"{self.url}{self.bot_token}/setMyCommands",
            json={
                "commands": commands
            }
        )

    def get_updates(self, path):
        params = {}
        if self._offset:
            params["offset"] = self._offset
        resp = self._send_request(
            url=f"{self.url}{self.bot_token}/getUpdates",
            params=params,
        )
        data = resp.json()["result"]
        # если офсет уже был, значит первое сообщение мы уже читали
        if self._offset > 1:
            data = data[1:]
        else:
            # если это первый запрос, то оставляем последнее сообщение, чтобы взять с него offset
            self._offset = data[-1]["update_id"]
            data = []
        # если есть новые сообщения - то двигаем оффсет
        if len(data) > 0:
            self._offset = data[-1]["update_id"]

        if data != []:
            try:
                if data[-1]["message"]["document"]['file_id']:
                    resp = self._send_request(
                        url=f"{self.url}{self.bot_token}/getFile?file_id={data[-1]['message']['document']['file_id']}",
                    )
                    file = resp.json()

                    urllib.request.urlretrieve(f"https://api.telegram.org/file/bot{self.bot_token}/{file['result']['file_path']}", f"{path}/{data[-1]['message']['document']['file_name']}")
                    print('+')
            except:
                print(data[-1]['message']['text'])
        return data

    def get_commands(self, path) -> List[str]:
        messages = self.get_updates(path)
        commands = []
        for message in messages:
            is_cmd = next((True for ent in message.get("message", {}).get("entities", {}) if ent.get("type") == "bot_command"), False)
            if is_cmd:
                commands.append(message["message"]["text"])
        return commands

    def _send_request(self, **kwargs):
        resp = requests.post(
            **kwargs
        )
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise TelegramConnectorException(f'Нерпавильно настроена связь с телеграмм: {ex}')
        return resp
