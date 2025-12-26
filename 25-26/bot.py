# bot.py - полностью рабочая версия
"""
Telegram бот для задач 1, 4, 5.
Интегрирует алгоритмы из task_1.py, task_4.py, task_5.py
"""

import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Импорт функций из task-файлов
try:
    # Импортируем функции для задания 1 из task_1.py
    from task_1 import execute_task_1_algorithm
except ImportError:
    # Если импорт не удался, используем локальные функции
    logger.warning("task_1.py не найден, используем локальные функции для задания 1")
    
    def execute_task_1_algorithm(arr1: list[int], arr2: list[int]) -> tuple:
        """Основной алгоритм задания 1 (локальная версия)."""
        logger.info(f"Задача 1: arr1={arr1}, arr2={arr2}")
        
        if len(arr1) != len(arr2):
            raise Exception(f"Массивы должны быть одинаковой длины. Длина первого: {len(arr1)}, второго: {len(arr2)}")
        
        if not arr1 or not arr2:
            raise Exception("Массив не может быть пустым")
        
        try:
            a = sorted(arr1, reverse=True)
            b = sorted(arr2)
            
            result = []
            for i in range(len(a)):
                if a[i] == b[i]:
                    result.append(0)
                else:
                    result.append(a[i] + b[i])
            
            result = sorted(result)
            logger.info(f"Результат: {result}")
            return result, a, b
            
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            raise Exception(f"Ошибка вычислений: {e}")

# Определяем функции для заданий 4 и 5
# В реальном коде они должны импортироваться из соответствующих файлов
def execute_task_4_algorithm(arr1: list[int], arr2: list[int], operation: str) -> list:
    """Основной алгоритм задания 4."""
    logger.info(f"Задача 4: {arr1} {operation} {arr2}")
    
    try:
        def digits_to_number(digits: list[int]) -> int:
            if not digits:
                return 0
            return int(''.join(map(str, digits)))
        
        num1 = digits_to_number(arr1)
        num2 = digits_to_number(arr2)
        
        if operation == '+':
            result = num1 + num2
        else:  # operation == '-'
            result = num1 - num2
        
        if result < 0:
            result_digits = ['-'] + [int(d) for d in str(abs(result))]
        else:
            result_digits = [int(d) for d in str(result)]
        
        logger.info(f"Результат: {result_digits}")
        return result_digits
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise Exception(f"Ошибка вычислений: {e}")

def execute_task_5_algorithm(arr: list[int], target_sum: int) -> int:
    """Основной алгоритм задания 5."""
    logger.info(f"Задача 5: массив={arr}, сумма={target_sum}")
    
    try:
        count = 0
        n = len(arr)
        
        if n == 0:
            return 0
        
        for i in range(n):
            current_sum = 0
            for j in range(i, n):
                current_sum += arr[j]
                if current_sum == target_sum:
                    count += 1
        
        logger.info(f"Найдено подмассивов: {count}")
        return count
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise Exception(f"Ошибка вычислений: {e}")

# === ИНИЦИАЛИЗАЦИЯ БОТА ===
TOKEN = "8525462952:AAFx6PjQFg08wK5FpMsknLcbO0FebBhyTzc"

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

# === СОЗДАНИЕ КЛАВИАТУР (КНОПОК) ===
# Функции для создания клавиатур с кнопками

def get_main_keyboard():
    """Создает главное меню с кнопками выбора задания"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Задание 1")],
            [KeyboardButton(text="Задание 4")],
            [KeyboardButton(text="Задание 5")],
            [KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите задание"
    )

def get_task1_keyboard():
    """Клавиатура для меню задания 1"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ввести массивы")],
            [KeyboardButton(text="Сгенерировать")],
            [KeyboardButton(text="Выполнить расчет")],
            [KeyboardButton(text="Показать результат")],
            [KeyboardButton(text="В главное меню")],
        ],
        resize_keyboard=True
    )

def get_task4_keyboard():
    """Клавиатура для меню задания 4"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ввести числа")],
            [KeyboardButton(text="Сгенерировать")],
            [KeyboardButton(text="Выбрать операцию")],
            [KeyboardButton(text="Выполнить расчет")],
            [KeyboardButton(text="Показать результат")],
            [KeyboardButton(text="В главное меню")],
        ],
        resize_keyboard=True
    )

def get_task5_keyboard():
    """Клавиатура для меню задания 5"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ввести массив")],
            [KeyboardButton(text="Ввести сумму")],
            [KeyboardButton(text="Сгенерировать")],
            [KeyboardButton(text="Выполнить расчет")],
            [KeyboardButton(text="Показать результат")],
            [KeyboardButton(text="В главное меню")],
        ],
        resize_keyboard=True
    )

# === УПРОЩЕННЫЙ FSM ===
# Хранит состояние каждого пользователя
user_states = {}

# === ОБРАБОТЧИКИ СООБЩЕНИЙ ===
# Обработчики команд и кнопок

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    
    # Инициализация состояния пользователя
    user_states[user_id] = {
        "state": "MAIN_MENU",
        "task1": {"arr1": None, "arr2": None, "result": None, "sorted1": None, "sorted2": None},
        "task4": {"arr1": None, "arr2": None, "operation": None, "result": None},
        "task5": {"arr": None, "target_sum": None, "result": None}
    }
    
    await message.answer(
        "Привет! Я бот для работы с массивами.\n\n"
        "Доступные задания:\n"
        "1. Задание 1 - Обработка двух массивов\n"
        "2. Задание 4 - Арифметика чисел-массивов\n"
        "3. Задание 5 - Подмассивы с заданной суммой\n\n"
        "Выберите задание для работы:",
        reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "/help")
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "Справка по боту\n\n"
        "Основные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать справку\n\n"
        "Доступные задания:\n"
        "1. Задание 1 - Обработка двух массивов\n"
        "2. Задание 4 - Арифметика чисел-массивов\n"
        "3. Задание 5 - Подмассивы с заданной суммой\n\n"
        "Используйте кнопки для навигации."
    )
    await message.answer(help_text)

@dp.message(F.text == "Помощь")
async def cmd_help_button(message: Message):
    """Обработчик кнопки помощи"""
    await cmd_help(message)

# === ОБРАБОТЧИКИ ДЛЯ ЗАДАНИЯ 1 ===

@dp.message(F.text == "Задание 1")
async def task1_menu(message: Message):
    """Показывает меню задания 1"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK1_MENU"}
    else:
        user_states[user_id]["state"] = "TASK1_MENU"
    
    await message.answer(
        "Задание 1: Обработка двух массивов\n\n"
        "Алгоритм:\n"
        "1. Сортировка первого массива по убыванию\n"
        "2. Сортировка второго массива по возрастанию\n"
        "3. Поэлементное сложение (при равенстве = 0)\n"
        "4. Сортировка результата\n\n"
        "Выберите действие:",
        reply_markup=get_task1_keyboard()
    )

@dp.message(F.text == "Ввести массивы")
async def task1_input_arrays(message: Message):
    """Запрашивает ввод массивов для задания 1"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK1_INPUT"}
    else:
        user_states[user_id]["state"] = "TASK1_INPUT"
    
    await message.answer(
        "Введите два массива через ; (пример: 1 2 3;4 5 6)\n"
        "Массивы должны быть одинаковой длины!"
    )

@dp.message(F.text == "Сгенерировать")
async def task1_generate_arrays(message: Message):
    """Генерирует случайные массивы для задания 1"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"task1": {}}
    
    # Генерация двух массивов по 5 случайных чисел
    arr1 = [random.randint(-10, 10) for _ in range(5)]
    arr2 = [random.randint(-10, 10) for _ in range(5)]
    
    # Сохраняем массивы в состоянии пользователя
    if "task1" not in user_states[user_id]:
        user_states[user_id]["task1"] = {}
    
    user_states[user_id]["task1"]["arr1"] = arr1
    user_states[user_id]["task1"]["arr2"] = arr2
    user_states[user_id]["state"] = "TASK1_MENU"
    
    await message.answer(
        f"Массивы сгенерированы\n\n"
        f"Массив 1: {arr1}\n"
        f"Массив 2: {arr2}",
        reply_markup=get_task1_keyboard()
    )

@dp.message(F.text == "Выполнить расчет")
async def task1_calculate(message: Message):
    """Выполняет расчет для задания 1"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли данные для расчета
    if user_id not in user_states or "task1" not in user_states[user_id]:
        await message.answer("Сначала введите или сгенерируйте массивы!")
        return
    
    task1_data = user_states[user_id]["task1"]
    
    if task1_data.get("arr1") is None or task1_data.get("arr2") is None:
        await message.answer("Сначала введите или сгенерируйте массивы!")
        return
    
    try:
        # Выполняем алгоритм из task_1.py
        result, sorted1, sorted2 = execute_task_1_algorithm(
            task1_data["arr1"], 
            task1_data["arr2"]
        )
        
        # Сохраняем результат
        user_states[user_id]["task1"]["result"] = result
        user_states[user_id]["task1"]["sorted1"] = sorted1
        user_states[user_id]["task1"]["sorted2"] = sorted2
        
        await message.answer(
            f"Расчет выполнен\n\n"
            f"Теперь можно посмотреть результат.",
            reply_markup=get_task1_keyboard()
        )
    except Exception as e:
        await message.answer(f"Ошибка вычисления: {e}")

@dp.message(F.text == "Показать результат")
async def task1_show_result(message: Message):
    """Показывает результат задания 1"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли результат
    if user_id not in user_states or "task1" not in user_states[user_id]:
        await message.answer("Сначала выполните расчет!")
        return
    
    task1_data = user_states[user_id]["task1"]
    
    if task1_data.get("result") is None:
        await message.answer("Сначала выполните расчет!")
        return
    
    # Форматируем и выводим результат
    await message.answer(
        f"Результат задания 1\n\n"
        f"Исходные массивы:\n"
        f"• Массив 1: {task1_data['arr1']}\n"
        f"• Массив 2: {task1_data['arr2']}\n\n"
        f"После сортировки:\n"
        f"• Массив 1 (по убыванию): {task1_data['sorted1']}\n"
        f"• Массив 2 (по возрастанию): {task1_data['sorted2']}\n\n"
        f"Итоговый массив:\n{task1_data['result']}"
    )

# === ОБРАБОТЧИКИ ДЛЯ ЗАДАНИЯ 4 ===

@dp.message(F.text == "Задание 4")
async def task4_menu(message: Message):
    """Показывает меню задания 4"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK4_MENU"}
    else:
        user_states[user_id]["state"] = "TASK4_MENU"
    
    await message.answer(
        "Задание 4: Арифметика чисел-массивов\n\n"
        "Алгоритм:\n"
        "1. Ввод чисел в виде массивов цифр\n"
        "2. Выбор операции (+ или -)\n"
        "3. Выполнение арифметической операции\n"
        "4. Вывод результата в виде массива цифр\n\n"
        "Выберите действие:",
        reply_markup=get_task4_keyboard()
    )

@dp.message(F.text == "Ввести числа")
async def task4_input_numbers(message: Message):
    """Запрашивает ввод чисел для задания 4"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK4_INPUT_NUMBERS"}
    else:
        user_states[user_id]["state"] = "TASK4_INPUT_NUMBERS"
    
    await message.answer(
        "Введите два числа в виде массивов цифр через ;\n"
        "Пример: 1 2 3;4 5 6\n"
        "Первое число: 123\n"
        "Второе число: 456"
    )

@dp.message(F.text == "Сгенерировать")
async def task4_generate_numbers(message: Message):
    """Генерирует случайные числа для задания 4"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"task4": {}}
    
    # Генерация двух чисел (массивов цифр)
    # Генерируем числа от 100 до 999 для удобства
    num1 = random.randint(100, 999)
    num2 = random.randint(100, 999)
    
    # Преобразуем числа в массивы цифр
    arr1 = [int(d) for d in str(num1)]
    arr2 = [int(d) for d in str(num2)]
    
    # Сохраняем массивы в состоянии пользователя
    if "task4" not in user_states[user_id]:
        user_states[user_id]["task4"] = {}
    
    user_states[user_id]["task4"]["arr1"] = arr1
    user_states[user_id]["task4"]["arr2"] = arr2
    user_states[user_id]["state"] = "TASK4_MENU"
    
    await message.answer(
        f"Числа сгенерированы\n\n"
        f"Число 1 ({num1}): {arr1}\n"
        f"Число 2 ({num2}): {arr2}",
        reply_markup=get_task4_keyboard()
    )

@dp.message(F.text == "Выбрать операцию")
async def task4_select_operation(message: Message):
    """Предлагает выбрать операцию для задания 4"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK4_SELECT_OPERATION"}
    else:
        user_states[user_id]["state"] = "TASK4_SELECT_OPERATION"
    
    await message.answer(
        "Выберите операцию:\n\n"
        "Напишите + для сложения\n"
        "Напишите - для вычитания"
    )

@dp.message(F.text == "Выполнить расчет")
async def task4_calculate(message: Message):
    """Выполняет расчет для задания 4"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли данные для расчета
    if user_id not in user_states or "task4" not in user_states[user_id]:
        await message.answer("Сначала введите или сгенерируйте числа и выберите операцию!")
        return
    
    task4_data = user_states[user_id]["task4"]
    
    if task4_data.get("arr1") is None or task4_data.get("arr2") is None or task4_data.get("operation") is None:
        await message.answer("Сначала введите или сгенерируйте числа и выберите операцию!")
        return
    
    try:
        # Выполняем алгоритм
        result = execute_task_4_algorithm(
            task4_data["arr1"], 
            task4_data["arr2"],
            task4_data["operation"]
        )
        
        # Сохраняем результат
        user_states[user_id]["task4"]["result"] = result
        
        await message.answer(
            f"Расчет выполнен\n\n"
            f"Теперь можно посмотреть результат.",
            reply_markup=get_task4_keyboard()
        )
    except Exception as e:
        await message.answer(f"Ошибка вычисления: {e}")

@dp.message(F.text == "Показать результат")
async def task4_show_result(message: Message):
    """Показывает результат задания 4"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли результат
    if user_id not in user_states or "task4" not in user_states[user_id]:
        await message.answer("Сначала выполните расчет!")
        return
    
    task4_data = user_states[user_id]["task4"]
    
    if task4_data.get("result") is None:
        await message.answer("Сначала выполните расчет!")
        return
    
    # Форматируем и выводим результат
    operation_text = "сложение" if task4_data.get("operation") == "+" else "вычитание"
    await message.answer(
        f"Результат задания 4\n\n"
        f"Число 1: {task4_data['arr1']}\n"
        f"Число 2: {task4_data['arr2']}\n"
        f"Операция: {operation_text}\n\n"
        f"Результат: {task4_data['result']}"
    )

# === ОБРАБОТЧИКИ ДЛЯ ЗАДАНИЯ 5 ===

@dp.message(F.text == "Задание 5")
async def task5_menu(message: Message):
    """Показывает меню задания 5"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK5_MENU"}
    else:
        user_states[user_id]["state"] = "TASK5_MENU"
    
    await message.answer(
        "Задание 5: Подмассивы с заданной суммой\n\n"
        "Алгоритм:\n"
        "1. Ввод массива чисел\n"
        "2. Ввод целевой суммы\n"
        "3. Поиск всех подмассивов с заданной суммой\n"
        "4. Вывод количества найденных подмассивов\n\n"
        "Выберите действие:",
        reply_markup=get_task5_keyboard()
    )

@dp.message(F.text == "Ввести массив")
async def task5_input_array(message: Message):
    """Запрашивает ввод массива для задания 5"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK5_INPUT_ARRAY"}
    else:
        user_states[user_id]["state"] = "TASK5_INPUT_ARRAY"
    
    await message.answer(
        "Введите массив чисел через пробел\n"
        "Пример: 1 2 3 4 5"
    )

@dp.message(F.text == "Ввести сумму")
async def task5_input_sum(message: Message):
    """Запрашивает ввод суммы для задания 5"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"state": "TASK5_INPUT_SUM"}
    else:
        user_states[user_id]["state"] = "TASK5_INPUT_SUM"
    
    await message.answer(
        "Введите целевую сумму (целое число)\n"
        "Пример: 10"
    )

@dp.message(F.text == "Сгенерировать")
async def task5_generate(message: Message):
    """Генерирует случайные данные для задания 5"""
    user_id = message.from_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {"task5": {}}
    
    # Генерация массива
    arr = [random.randint(-5, 10) for _ in range(8)]
    # Генерация целевой суммы
    target_sum = random.randint(0, 20)
    
    # Сохраняем данные в состоянии пользователя
    if "task5" not in user_states[user_id]:
        user_states[user_id]["task5"] = {}
    
    user_states[user_id]["task5"]["arr"] = arr
    user_states[user_id]["task5"]["target_sum"] = target_sum
    user_states[user_id]["state"] = "TASK5_MENU"
    
    await message.answer(
        f"Данные сгенерированы\n\n"
        f"Массив: {arr}\n"
        f"Целевая сумма: {target_sum}",
        reply_markup=get_task5_keyboard()
    )

@dp.message(F.text == "Выполнить расчет")
async def task5_calculate(message: Message):
    """Выполняет расчет для задания 5"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли данные для расчета
    if user_id not in user_states or "task5" not in user_states[user_id]:
        await message.answer("Сначала введите или сгенерируйте массив и сумму!")
        return
    
    task5_data = user_states[user_id]["task5"]
    
    if task5_data.get("arr") is None or task5_data.get("target_sum") is None:
        await message.answer("Сначала введите или сгенерируйте массив и сумму!")
        return
    
    try:
        # Выполняем алгоритм
        result = execute_task_5_algorithm(
            task5_data["arr"], 
            task5_data["target_sum"]
        )
        
        # Сохраняем результат
        user_states[user_id]["task5"]["result"] = result
        
        await message.answer(
            f"Расчет выполнен\n\n"
            f"Теперь можно посмотреть результат.",
            reply_markup=get_task5_keyboard()
        )
    except Exception as e:
        await message.answer(f"Ошибка вычисления: {e}")

@dp.message(F.text == "Показать результат")
async def task5_show_result(message: Message):
    """Показывает результат задания 5"""
    user_id = message.from_user.id
    
    # Проверяем, есть ли результат
    if user_id not in user_states or "task5" not in user_states[user_id]:
        await message.answer("Сначала выполните расчет!")
        return
    
    task5_data = user_states[user_id]["task5"]
    
    if task5_data.get("result") is None:
        await message.answer("Сначала выполните расчет!")
        return
    
    # Форматируем и выводим результат
    await message.answer(
        f"Результат задания 5\n\n"
        f"Массив: {task5_data['arr']}\n"
        f"Целевая сумма: {task5_data['target_sum']}\n\n"
        f"Количество подмассивов с заданной суммой: {task5_data['result']}"
    )

@dp.message(F.text == "В главное меню")
async def back_to_main(message: Message):
    """Возвращает в главное меню"""
    user_id = message.from_user.id
    if user_id in user_states:
        user_states[user_id]["state"] = "MAIN_MENU"
    
    await message.answer(
        "Главное меню\n\n"
        "Выберите задание для работы:",
        reply_markup=get_main_keyboard()
    )

# === ОБРАБОТЧИК ТЕКСТОВОГО ВВОДА ===
# Обрабатывает текстовый ввод для всех заданий

@dp.message()
async def handle_text_input(message: Message):
    """Обработчик текстового ввода"""
    user_id = message.from_user.id
    text = message.text.strip()
    
    if user_id not in user_states:
        await message.answer("Используйте /start для начала работы")
        return
    
    state = user_states[user_id].get("state", "MAIN_MENU")
    
    # Обработка ввода для задания 1
    if state == "TASK1_INPUT":
        try:
            arr1_text, arr2_text = text.split(";")
            arr1 = list(map(int, arr1_text.strip().split()))
            arr2 = list(map(int, arr2_text.strip().split()))
            
            if len(arr1) != len(arr2):
                await message.answer("Массивы должны быть одинаковой длины!")
                return
            
            if "task1" not in user_states[user_id]:
                user_states[user_id]["task1"] = {}
            
            user_states[user_id]["task1"]["arr1"] = arr1
            user_states[user_id]["task1"]["arr2"] = arr2
            user_states[user_id]["state"] = "TASK1_MENU"
            
            await message.answer(
                f"Массивы сохранены\n\n"
                f"Массив 1: {arr1}\n"
                f"Массив 2: {arr2}",
                reply_markup=get_task1_keyboard()
            )
        except Exception as e:
            await message.answer(f"Ошибка ввода: {e}\n\nПример: 1 2 3;4 5 6")
    
    # Обработка ввода для задания 4 (числа)
    elif state == "TASK4_INPUT_NUMBERS":
        try:
            arr1_text, arr2_text = text.split(";")
            arr1 = list(map(int, arr1_text.strip().split()))
            arr2 = list(map(int, arr2_text.strip().split()))
            
            if "task4" not in user_states[user_id]:
                user_states[user_id]["task4"] = {}
            
            user_states[user_id]["task4"]["arr1"] = arr1
            user_states[user_id]["task4"]["arr2"] = arr2
            user_states[user_id]["state"] = "TASK4_MENU"
            
            await message.answer(
                f"Числа сохранены\n\n"
                f"Число 1: {arr1}\n"
                f"Число 2: {arr2}\n\n"
                f"Теперь выберите операцию.",
                reply_markup=get_task4_keyboard()
            )
        except Exception as e:
            await message.answer(f"Ошибка ввода: {e}\n\nПример: 1 2 3;4 5 6")
    
    # Обработка выбора операции для задания 4
    elif state == "TASK4_SELECT_OPERATION":
        if text in ['+', '-']:
            if "task4" not in user_states[user_id]:
                user_states[user_id]["task4"] = {}
            
            user_states[user_id]["task4"]["operation"] = text
            user_states[user_id]["state"] = "TASK4_MENU"
            
            operation_text = "сложение" if text == '+' else "вычитание"
            await message.answer(
                f"Операция выбрана: {operation_text}\n\n"
                f"Теперь можно выполнить расчет.",
                reply_markup=get_task4_keyboard()
            )
        else:
            await message.answer("Введите '+' или '-'")
    
    # Обработка ввода массива для задания 5
    elif state == "TASK5_INPUT_ARRAY":
        try:
            arr = list(map(int, text.split()))
            
            if "task5" not in user_states[user_id]:
                user_states[user_id]["task5"] = {}
            
            user_states[user_id]["task5"]["arr"] = arr
            user_states[user_id]["state"] = "TASK5_MENU"
            
            await message.answer(
                f"Массив сохранен: {arr}\n\n"
                f"Теперь введите целевую сумму.",
                reply_markup=get_task5_keyboard()
            )
        except Exception as e:
            await message.answer(f"Ошибка ввода: {e}\n\nПример: 1 2 3 4 5")
    
    # Обработка ввода суммы для задания 5
    elif state == "TASK5_INPUT_SUM":
        try:
            target_sum = int(text)
            
            if "task5" not in user_states[user_id]:
                user_states[user_id]["task5"] = {}
            
            user_states[user_id]["task5"]["target_sum"] = target_sum
            user_states[user_id]["state"] = "TASK5_MENU"
            
            await message.answer(
                f"Целевая сумма сохранена: {target_sum}\n\n"
                f"Теперь можно выполнить расчет.",
                reply_markup=get_task5_keyboard()
            )
        except Exception as e:
            await message.answer(f"Ошибка ввода: {e}\n\nВведите целое число")
    
    # Обработка неизвестных команд
    else:
        await message.answer("Не понимаю команду. Используйте кнопки меню.")

# === ЗАПУСК БОТА ===
async def main():
    """Главная функция запуска бота"""
    logger.info("Бот запускается...")
    print("=" * 50)
    print("Бот запущен!")
    print("Откройте Telegram и найдите вашего бота")
    print("Используйте /start для начала работы")
    print("=" * 50)
    print("Бот работает... (Ctrl+C для остановки)")
    
    # Запускаем опрос обновлений от Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        # Запускаем асинхронную функцию main
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")
        logger.info("Bot stopped by user")
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")
        logger.error(f"Bot error: {e}")