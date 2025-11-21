import sys
import random # Для случайной генерации

dannie = None  
otvet = None    # Результат

def vvod_matr_ruchnoy(razmer):
    matr = []
    print(f"Вводим матрицу {razmer}x{razmer}:")
    for i in range(razmer):
        while True:
            try:
                stroka_str = input(f"Строка {i+1} (числа через пробел): ")
                chast_spiska = stroka_str.split()
                stroka = []
                for element in chast_spiska:
                    stroka.append(float(element))
                    
                if len(stroka) != razmer:
                    print(f"Ошибка: В строке должно быть {razmer} чисел. Попробуйте еще раз.")
                    continue
                matr.append(stroka)
                break
            except ValueError:
                print("Ошибка: Вводите только числа.")
    return matr

def vvod_matr_sluchayno(razmer):
    """Генерирует случайную матрицу (используя базовый random)."""
    matr = []
    for i in range(razmer):
        stroka = []
        for j in range(razmer):
            stroka.append(random.randint(-5, 5)) 
        matr.append(stroka)
    return matr

def vvod_dannyh():
    global dannie, otvet
    print("\n Ввод исходных данных ")
    
    # 1. Размер
    while True:
        try:
            razmer = int(input("Введите размер N для матриц NxN: "))
            if razmer <= 0:
                print("Размер должен быть больше нуля.")
                continue
            break
        except ValueError:
            print("Неверный ввод. Введите целое число.")

    # 2. Выбор режима
    while True:
        rezhim = input("Режим (1 - Ручной, 2 - Случайный): ")
        if rezhim == '1':
            print("\n Ввод Матрицы A ")
            matr_a = vvod_matr_ruchnoy(razmer)
            print("\n Ввод Матрицы B ")
            matr_b = vvod_matr_ruchnoy(razmer)
            break
        elif rezhim == '2':
            matr_a = vvod_matr_sluchayno(razmer)
            matr_b = vvod_matr_sluchayno(razmer)
            print(f"Сгенерированы две случайные матрицы {razmer}x{razmer}.")
            break
        else:
            print("Неверный выбор. Введите '1' или '2'.")

    dannie = [matr_a, matr_b]
    otvet = None # Сброс ответа
    print("\nДанные введены. Ответ сброшен.")
    print("Матрица A:")
    for row in matr_a:
        print(row)
    print("Матрица B:")
    for row in matr_b:
        print(row)

#  Функции для алгоритма (ручная реализация) 

def summa_matr(matr1, matr2):
    """Сложение двух матриц (ручная реализация)."""
    razmer = len(matr1)
    rez_matr = []
    for i in range(razmer):
        stroka = []
        for j in range(razmer):
            stroka.append(matr1[i][j] + matr2[i][j])
        rez_matr.append(stroka)
    return rez_matr

def get_minor(matr, i, j):
    """Получение минора (для определителя)."""
    razmer = len(matr)
    minor = []
    for row in range(razmer):
        if row != i:
            new_row = []
            for col in range(razmer):
                if col != j:
                    new_row.append(matr[row][col])
            minor.append(new_row)
    return minor

def opredelitel(matr):
    """Вычисление определителя (рекурсивная ручная реализация)."""
    razmer = len(matr)
    
    if razmer == 1:
        return matr[0][0]
    
    if razmer == 2:
        return matr[0][0] * matr[1][1] - matr[0][1] * matr[1][0]
    
    # Для больших матриц - рекурсия
    det = 0
    for j in range(razmer):
        minor = get_minor(matr, 0, j)
        det += ((-1) ** j) * matr[0][j] * opredelitel(minor)
        
    return det

#  Основная функция алгоритма 

def algoritm():
    """
    Меню 2: Выполнение алгоритма. Реализовано вручную.
    """
    global dannie, otvet
    print("\n Запуск алгоритма (Итерация 3: Реализовано вручную) ")
    if dannie is None:
        print("ОШИБКА: Сначала введите данные (пункт 1).")
        return

    matr_a, matr_b = dannie
    
    # 1. Сумма матриц
    summa = summa_matr(matr_a, matr_b)
    
    # 2. Определитель суммы матриц
    try:
        opr = opredelitel(summa)
    except Exception as e:
        opr = f"Ошибка при расчете определителя: {e}"
        
    otvet = {
        'summa': summa, 
        'opredelitel': opr
    }
    print("Алгоритм отработал. Ответ сохранен.")

def pokazat_otvet():
    """
    Меню 3: Показать ответ.
    """
    print("\n Показать ответ ")
    if otvet is None:
        print("ОШИБКА: Сначала запустите алгоритм (пункт 2).")
        return

    print("Результат:")
    print("Сумма матриц (A + B):")
    for row in otvet['summa']:
        print(row)
    print(f"Определитель суммы матриц: {otvet['opredelitel']}")

def vyhod():
    """
    Меню 4: Выход.
    """
    print("\n Выход из программы ")
    sys.exit(0)

def glavnoe_menu():
    """
    Главный цикл программы.
    """
    while True:
        print("\nМЕНЮ (Итерация 3) ")
        print("1. Ввод данных")
        print("2. Запуск алгоритма")
        print("3. Показать ответ")
        print("4. Выход")

        vybor = input("Ваш выбор (1-4): ")

        if vybor == '1':
            vvod_dannyh()
        elif vybor == '2':
            algoritm()
        elif vybor == '3':
            pokazat_otvet()
        elif vybor == '4':
            vyhod()
        else:
            print("Неправильный выбор. Попробуйте еще раз.")

if __name__ == "__main__":
    glavnoe_menu()