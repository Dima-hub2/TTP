# Итерация 2: меню + ввод, алгоритм — заглушка

import random

# Глобальные переменные
matrix_a = None
matrix_b = None
result = None

def show_menu():
    print("   МАТРИЧНЫЙ КАЛЬКУЛЯТОР")
    print("1. Ввод данных")
    print("2. Выполнить алгоритм")
    print("3. Показать результат")
    print("0. Выход")

def input_data():
    global matrix_a, matrix_b, result
    result = None  # сбрасываем результат
    try:
        n = int(input("Введите размер матриц (n): "))
        if n <= 0:
            print("Размер должен быть > 0!")
            return
    except:
        print("Введите число!")
        return

    print("1. Вручную")
    print("2. Случайно")
    choice = input("Выбор: ").strip()

    if choice == "1":
        print(f"Введите матрицу A ({n}x{n}), по строкам через пробел:")
        matrix_a = []
        for _ in range(n):
            row = list(map(int, input().split()))
            if len(row) != n:
                print("Ошибка: строка должна содержать", n, "чисел")
                return
            matrix_a.append(row)
        
        print(f"Введите матрицу B ({n}x{n}):")
        matrix_b = []
        for _ in range(n):
            row = list(map(int, input().split()))
            if len(row) != n:
                print("Ошибка в строке B")
                return
            matrix_b.append(row)
    else:
        matrix_a = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
        matrix_b = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
        print("Матрицы сгенерированы случайным образом!")
    
    print("Данные успешно введены!")

def run_algorithm():
    global result
    if matrix_a is None or matrix_b is None:
        print("Ошибка: сначала введите данные!")
        return
    result = "сумма и определитель (алгоритм будет здесь)"
    print("Алгоритм выполнен (заглушка)!")
    return result

def show_result():
    if result is None:
        print("Ошибка: сначала выполните алгоритм!")
        return
    print(f"Результат: {result}")

def main():
    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            input_data()
        elif choice == "2":
            run_algorithm()
        elif choice == "3":
            show_result()
        elif choice == "0":
            print("Программа завершена. До свидания!")
            break
        else:
            print("Неверный выбор! Используйте 0–3.")

if __name__ == "__main__":
    main()