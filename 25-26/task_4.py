"""
Task 2 — проверка условия a[i] + b[i] == c[i] и вычисление степени (FSM-корутина)

Модуль реализует функциональность задачи 2, состоящую из:
    1) Вспомогательных функций: генерации массива и вычисления выражений.
    2) Конечного автомата, реализованного через корутину (task2_fsm).

Функциональность задачи:
    - ввод трёх массивов вручную;
    - генерация трёх случайных массивов одинаковой длины;
    - проверка элементов: arr1[i] + arr2[i] == arr3[i];
    - вычисление выражения:
          (arr1[i] + arr2[i] + arr3[i]) ** min(arr1[i], arr2[i], arr3[i])
    - вывод списка результатов;
    - изменение состояний FSM;
    - отключение логирования.

Состояния FSM:
    NO_DATA     — массивы ещё не заданы;
    HAS_DATA    — массивы получены, но вычисления не выполнены;
    HAS_RESULT  — вычисление выполнено и результат сохранён.

Публичный API:
    task2_fsm() — запускает FSM задачи 2.

Вспомогательные функции:
    - generate_array(size, min_v, max_v)
        Генерация случайного массива.
    - sum_and_power(arr1, arr2, arr3)
        Выполняет проверку суммы и вычисление степени.
"""

import random
from messages import MESSAGES
from logger import logger
from exceptions import DataNotSetError, InvalidValueError, OperationError, InputError

msgs = MESSAGES["task2"]


def generate_array(size: int, min_v: int = 0, max_v: int = 50) -> list[int]:
    """Генерирует массив случайных чисел указанного размера.

    Параметры:
        size (int): длина массива (должна быть > 0)
        min_v (int): минимальное значение
        max_v (int): максимальное значение

    Исключения:
        InvalidValueError: если size <= 0
    """

    if size <= 0:
        raise InvalidValueError("Размер массива должен быть положительным")
    logger.info("generating a random array")
    return [random.randint(min_v, max_v) for _ in range(size)]


def sum_and_power(arr1: list[int], arr2: list[int], arr3: list[int]) -> list[dict]:
    """
    Для трёх массивов одинаковой длины проверяет, где:
        arr1[i] + arr2[i] == arr3[i]
    и вычисляет выражение:
        (arr1[i] + arr2[i] + arr3[i]) ** min(arr1[i], arr2[i], arr3[i])

    Параметры:
        arr1 (list[int]): Первый массив.
        arr2 (list[int]): Второй массив.
        arr3 (list[int]): Третий массив.

    Возвращает:
        list[dict]:
            Каждый элемент — словарь вида:
            {
                "index": i,
                "sum": arr1[i] + arr2[i] + arr3[i],
                "power": (sum) ** min(arr1[i], arr2[i], arr3[i])
            }

    Исключения:
        DataNotSetError: если массивы не одинаковой длины или пустые
        OperationError: при ошибках вычисления степени
    """

    logger.info("task2: sum_and_power()")

    if not arr1 or not arr2 or not arr3:
        raise DataNotSetError("Массивы не заданы или пусты")
    if len(arr1) != len(arr2) or len(arr2) != len(arr3):
        raise DataNotSetError("Все массивы должны быть одинаковой длины")

    results = []
    try:
        for i, (a, b, c) in enumerate(zip(arr1, arr2, arr3)):
            if a + b == c:
                total = a + b + c
                power = total ** min(a, b, c)
                results.append({
                    "index": i,
                    "sum": total,
                    "power": power
                })
                logger.debug(f"Index {i}: a={a}, b={b}, c={c}, sum={total}, power={power}")
    except Exception as e:
        raise OperationError(f"Ошибка вычисления степени: {e}") from e

    return results


def task2_fsm():
    """
    Корутина конечного автомата задачи 2.

    Управляет вводом трёх массивов, их генерацией,
    выполнением проверки суммы и возведения в степень,
    выводом результата и состояниями FSM.

    Состояния:
        NO_DATA   — массивы не заданы
        HAS_DATA  — массивы заданы
        HAS_RESULT — выполнены вычисления

    Yields
        None: Ожидание пользовательского выбора пункта меню.

    Returns
        None: Возврат в главное меню.
    """

    arr1 = None
    arr2 = None
    arr3 = None
    result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = yield
        logger.info(f"task2 choice={choice}, state={state}")

        if choice == "5":
            return
