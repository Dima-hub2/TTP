# file name: messages.py
# file content begin
"""
messages.py

Централизованный словарь сообщений для всего приложения.
Сообщения сгруппированы по задачам: main_menu, task1, task2, task3.
"""

class Messages:
    """Централизованные сообщения для всех меню и FSM."""

    class MENU_MAIN:
        title = "=== ГЛАВНОЕ МЕНЮ ==="
        options = [
            "1. Задание 1 ",
            "2. Задание 2 ",
            "3. Задание 3 ",
            "0. Выход"
        ]
        prompt = "Выберите пункт: "
        invalid = "Неверный пункт!"
        exit_msg = "Выход из программы..."

    class TASK1:
        title = "=== ЗАДАНИЕ 1 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Подсчитать общие числа с учётом реверса",
            "4. Показать результат",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        calculation_done = "Подсчёт выполнен."
        no_data = "Сначала введите массивы!"
        invalid_choice = "Неверный пункт!"

    class TASK2:
        title = "=== ЗАДАНИЕ 2 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Найти индексы, где arr1+arr2==arr3, и возвести суммы в степень",
            "4. Показать массивы и результаты",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        calculation_done = "Вычисления выполнены."
        no_data = "Сначала введите массивы!"
        invalid_choice = "Неверный пункт!"

    class TASK3:
        title = "=== ЗАДАНИЕ 3 ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Выполнить подсчет",
            "4. Показать результат",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        calculation_done = "Операция выполнена."
        no_data = "Массивы ещё не введены или не сгенерированы!"
        invalid_choice = "Неверный пункт!"

# Сообщения для Telegram бота
class TelegramMessages:
    """Сообщения для Telegram бота."""
    
    # Общие сообщения
    WELCOME = " Добро пожаловать в бот для работы с массивами!\nВыберите задание:"
    HELP = (
        " *Справка по боту*\n\n"
        "Используйте кнопки для навигации.\n"
        "Каждое задание имеет своё меню с опциями."
    )
    UNKNOWN = "Не понимаю команду. Используйте кнопки меню."
    
    # Задание 1
    TASK1_TITLE = " *Задание 1: Подсчёт общих и «перевёрнутых» чисел*"
    TASK1_INPUT = "Введите два массива через ; (пример: 1 2 3;4 5 6)"
    TASK1_SAVED = " Массивы сохранены"
    TASK1_GENERATED = " Массивы сгенерированы"
    TASK1_CALCULATED = " Вычисления выполнены"
    TASK1_NO_DATA = " Сначала введите массивы!"
    TASK1_NO_RESULT = " Сначала выполните расчёт!"
    
    # Задание 2
    TASK2_TITLE = " *Задание 2: Проверка суммы и возведение в степень*"
    TASK2_INPUT = "Введите три массива через ; (пример: 1 2 3;4 5 6;5 7 9)"
    TASK2_SAVED = " Массивы сохранены"
    TASK2_GENERATED = " Массивы сгенерированы"
    TASK2_CALCULATED = " Вычисления выполнены"
    TASK2_NO_DATA = " Сначала введите массивы!"
    TASK2_NO_RESULT = " Сначала выполните расчёт!"
    TASK2_NO_MATCHES = "ℹ Совпадений не найдено"
    
    # Задание 3
    TASK3_TITLE = " *Задание 3: Сортировка и поэлементное сложение*"
    TASK3_INPUT = "Введите два массива через ; (пример: 1 2 3;4 5 6)"
    TASK3_SAVED = " Массивы сохранены"
    TASK3_GENERATED = " Массивы сгенерированы"
    TASK3_CALCULATED = " Операция выполнена"
    TASK3_NO_DATA = " Сначала введите массивы!"
    TASK3_NO_RESULT = " Сначала выполните расчёт!"

# Совместимость со старым стилем
MESSAGES = {
    "main_menu": {
        "title": Messages.MENU_MAIN.title,
        "options": Messages.MENU_MAIN.options,
        "prompt": Messages.MENU_MAIN.prompt,
        "invalid": Messages.MENU_MAIN.invalid,
        "exit": Messages.MENU_MAIN.exit_msg
    },
    "task1": {
        "title": Messages.TASK1.title,
        "menu": Messages.TASK1.menu,
        "prompt": Messages.TASK1.prompt,
        "input_error": Messages.TASK1.input_error,
        "calculation_done": Messages.TASK1.calculation_done,
        "no_data": Messages.TASK1.no_data,
        "invalid_choice": Messages.TASK1.invalid_choice
    },
    "task2": {
        "title": Messages.TASK2.title,
        "menu": Messages.TASK2.menu,
        "prompt": Messages.TASK2.prompt,
        "input_error": Messages.TASK2.input_error,
        "calculation_done": Messages.TASK2.calculation_done,
        "no_data": Messages.TASK2.no_data,
        "invalid_choice": Messages.TASK2.invalid_choice
    },
    "task3": {
        "title": Messages.TASK3.title,
        "menu": Messages.TASK3.menu,
        "prompt": Messages.TASK3.prompt,
        "input_error": Messages.TASK3.input_error,
        "calculation_done": Messages.TASK3.calculation_done,
        "no_data": Messages.TASK3.no_data,
        "invalid_choice": Messages.TASK3.invalid_choice
    }
}
# file content end