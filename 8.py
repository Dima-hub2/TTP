import sys

dannie = None  # Исходные данные
otvet = None    # Результат

def vvod_dannyh():
    global dannie, otvet
    print("--- Ввод данных (Заглушка) ---")
    # Имитация ввода
    dannie = "Матрицы готовы"
    otvet = None # Сброс ответа
    print("Данные введены. Ответ сброшен.")
    return dannie

def algoritm():
    global dannie, otvet
    print("--- Запуск алгоритма (Заглушка) ---")
    if dannie is None:
        print("ОШИБКА: Сначала введите данные (пункт 1).")
        return None

    # Имитация работы
    otvet = "Сумма и определитель посчитаны"
    print("Алгоритм отработал.")
    return otvet

def pokazat_otvet():
    print("--- Показать ответ (Заглушка) ---")
    if otvet is None:
        print("ОШИБКА: Сначала запустите алгоритм (пункт 2).")
        return

    print(f"Ответ: {otvet}")

def vyhod():
    print("--- Выход из программы ---")
    sys.exit(0)

def glavnoe_menu():
    while True:
        print("\nМЕНЮ (Итерация 1) ")
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