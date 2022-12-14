# TemplateTelegramBot
___
### Описание
Базовый шаблон бота Telegram, основанный на `aiogram 3.x` с использованием ORM `sqlalchemy 1.4`. Так же в данной 
реализации подразумевается использование `PostgreSQL` в качестве базы данных с использованием асинхронного драйвера 
`asyncpg`. Но при желании не должно возникнуть проблем сменить драйвер и базу данных на желаемые.

### Как начать:

1. Убедиться, что версия Python 3.8.x или новее:
> `py --version`
3. Обновить `pip`, `setuptools`, `wheel`:
> `py -m pip install --upgrade pip setuptools wheel`
2. Клонировать проект в желаемую директорию:
> `git clone https://github.com/Mempron/TemplateTelegramBot`
3. Перейти в клонированную директорию (перед этим при желании переименовать директорию):
> `cd TemplateTemplateBot`
4. Создать виртуальное окружение `venv`:
> `py -m venv venv`
5. Активировать виртуальное окружение:
> `env\Scripts\activate`
6. Установить зависимости проекта в `venv`:
> `pip install -r requirements.txt`
7. Запуск:
> `python main.py`
