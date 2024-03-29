import json
import pathlib
from json import JSONDecodeError

try:
    import pyautogui

except:
    import os
    os.system('pip install PyAutoGUI')
    os.system('pip install pyscreeze')
    os.system('pip install pillow')

try:
    import win32api

except:
    import os
    os.system('pip install pywin32')

from .printers.console import ConsolePrinter
from .printers.tg_printer import TelegramPrinter
from .printers.window import WindowPrinter
from .processor import Processor
from .printers.base_printer import Level
from .telegram_connector import TelegramConnector


def init_processor():
    try:
        config = {
  "bot_token": "6722982894:AAGdHkbU5BoPorK7NFlbIBiJKbWJEZ0YxnI",
  "chat_id": "5337729489",
  "push_message_btn": 36
}
    except FileNotFoundError:
        raise ValueError('Не вижу файл конфига')
    except JSONDecodeError:
        raise ValueError('Ошибка в настройки конфиг файла')
    else:
        try:
            tg_connector = TelegramConnector(config)
            printer = {
                'console': ConsolePrinter,
                'telegram': TelegramPrinter,
                'window': WindowPrinter,
            }[config.get('printer', 'telegram')](
                config,
                level=Level.INFO,
                tg_connector=tg_connector
            )
            return Processor(config, printer, tg_connector)
        except ValueError:
            raise


def st(path):
    try:
        processor = init_processor()
    except ValueError as ex:
        print(ex)
        pyautogui.alert(text=str(ex), title='Ошибка', button='OK, поправлю')
        exit(9)
    else:
        processor.run_loop(path)
