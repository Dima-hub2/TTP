import random
import sys

def get_matrix_size():
    """
    Запрашивает у пользователя размер квадратной матрицы (N) и проверяет ввод.
    """
    while True:
        try:
            size = int(input("Введите размер квадратной матрицы N (целое число > 0): "))
            if size > 0:
                return size
            else:
                print("Размер должен быть положительным числом.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")

def create_matrix_manual(size):
    """
    Позволяет пользователю вручную ввести элементы матрицы N x N.
    """
    matrix = []
    print(f"Введите элементы матрицы {size}x{size} построчно:")
    for i in range(size):
        while True:
            try:
                row_str = input(f"Строка {i+1} (элементы через пробел): ")
                row = [float(x) for x in row_str.split()]
                if len(row) == size:
                    matrix.append(row)
                    break
                else:
                    print(f"Ошибка: Введите ровно {size} элементов.")
            except ValueError:
                print("Некорректный ввод. Убедитесь, что все элементы - числа.")
    return matrix

def create_matrix_random(size):
    """
    Генерирует случайную матрицу N x N с целыми числами от -10 до 10.
    """
    matrix = []
    for _ in range(size):
        row = [random.randint(-10, 10) for _ in range(size)]
        matrix.append(row)
    return matrix

def add_matrices(matrix_a, matrix_b):
    """
    Складывает две матрицы одинакового размера.
    """
    size = len(matrix_a)
    sum_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(matrix_a[i][j] + matrix_b[i][j])
        sum_matrix.append(row)
    return sum_matrix

def calculate_determinant(matrix):
    """
    Вычисляет определитель квадратной матрицы (рекурсивный метод).
    Поддерживает матрицы до 3x3 для простоты, как было запрошено.
    Для матриц большего размера требуется более сложный алгоритм (например, LU-разложение).
    """
    size = len(matrix)
    
    if size == 1:
        return matrix[0][0]
    
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    if size == 3:
        det = (matrix[0][0] * matrix[1][1] * matrix[2][2] +
               matrix[0][1] * matrix[1][2] * matrix[2][0] +
               matrix[0][2] * matrix[1][0] * matrix[2][1] -
               matrix[0][2] * matrix[1][1] * matrix[2][0] -
               matrix[0][1] * matrix[1][0] * matrix[2][2] -
               matrix[0][0] * matrix[1][2] * matrix[2][1])
        return det

    det = 0
    for c in range(size):
        # Вычисление минора
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        # Рекурсивный вызов
        cofactor = matrix[0][c] * calculate_determinant(minor)
        # Применение знака
        if c % 2 == 0:
            det += cofactor
        else:
            det -= cofactor
    return det

def print_matrix(matrix, name="Матрица"):
    """
    Аккуратно выводит матрицу на консоль.
    """
    print(f"\n--- {name} ---")
    if not matrix:
        print("Матрица пуста.")
        return
        
    # Находим максимальную ширину для форматирования
    max_width = 0
    for row in matrix:
        for element in row:
            max_width = max(max_width, len(f"{element:.2f}"))

    for row in matrix:
        row_str = " | ".join(f"{element:>{max_width}.2f}" for element in row)
        print(f"| {row_str} |")
    print("-" * (len(row_str) + 4))

def display_menu():
    """
    Отображает главное меню приложения и запрашивает выбор.
    """
    print("\n" + "="*40)
    print("Консольное приложение: Операции с матрицами")
    print("="*40)
    print("1. Ввод исходных данных (вручную или случайно)")
    print("2. Выполнение алгоритма (Сумма матриц и Определитель)")
    print("3. Вывод результата")
    print("4. Завершение работы программы")
    print("="*40)
    return input("Выберите пункт меню (1-4): ")

def input_data(state):
    """
    Обрабатывает ввод исходных данных, обновляет состояние и сбрасывает результаты.
    """
    print("\n--- Ввод исходных данных ---")
    
    # 1. Получение размера
    size = get_matrix_size()
    
    # 2. Выбор способа ввода
    while True:
        mode = input("Выберите способ ввода (1 - Вручную, 2 - Случайно): ")
        if mode == '1':
            print("\n--- Ввод Матрицы A ---")
            matrix_a = create_matrix_manual(size)
            print("\n--- Ввод Матрицы B ---")
            matrix_b = create_matrix_manual(size)
            break
        elif mode == '2':
            matrix_a = create_matrix_random(size)
            matrix_b = create_matrix_random(size)
            print("Матрицы A и B успешно сгенерированы случайным образом.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите '1' или '2'.")

    # Обновление состояния
    state['matrix_a'] = matrix_a
    state['matrix_b'] = matrix_b
    state['data_ready'] = True
    state['algorithm_executed'] = False # Сброс результатов
    state['sum_matrix'] = None
    state['determinant'] = None
    
    print_matrix(matrix_a, "Матрица A (Введенные данные)")
    print_matrix(matrix_b, "Матрица B (Введенные данные)")
    print("\nИсходные данные успешно введены. Результаты предыдущих вычислений сброшены.")
    return state

def execute_algorithm(state):
    """
    Выполняет алгоритм: сложение матриц и вычисление определителя суммы.
    """
    print("\n--- Выполнение алгоритма ---")
    
    if not state['data_ready']:
        print("Ошибка: Исходные данные не введены. Пожалуйста, сначала выберите пункт 1.")
        return state

    matrix_a = state['matrix_a']
    matrix_b = state['matrix_b']
    
    # 1. Сложение матриц
    try:
        sum_matrix = add_matrices(matrix_a, matrix_b)
        print("Шаг 1: Сложение матриц выполнено успешно.")
    except Exception as e:
        print(f"Ошибка при сложении матриц: {e}")
        return state

    # 2. Вычисление определителя
    try:
        determinant = calculate_determinant(sum_matrix)
        print("Шаг 2: Вычисление определителя выполнено успешно.")
    except Exception as e:
        print(f"Ошибка при вычислении определителя: {e}")
        return state

    # Обновление состояния
    state['sum_matrix'] = sum_matrix
    state['determinant'] = determinant
    state['algorithm_executed'] = True
    
    print("\nАлгоритм выполнен. Результат готов к выводу.")
    return state

def display_result(state):
    """
    Выводит результат работы алгоритма.
    """
    print("\n--- Вывод результата ---")
    
    if not state['algorithm_executed']:
        print("Ошибка: Алгоритм не был выполнен. Пожалуйста, сначала выберите пункт 2.")
        return

    sum_matrix = state['sum_matrix']
    determinant = state['determinant']
    
    print("--- Результаты вычислений ---")
    print_matrix(sum_matrix, "Сумма матриц (A + B)")
    print(f"Определитель суммы матриц: {determinant:.4f}")
    print("----------------------------")

def main():
    """
    Основная функция приложения, управляющая циклом меню и состоянием.
    """
    # Инициализация состояния приложения
    state = {
        'matrix_a': None,
        'matrix_b': None,
        'sum_matrix': None,
        'determinant': None,
        'data_ready': False,
        'algorithm_executed': False
    }
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            state = input_data(state)
        
        elif choice == '2':
            state = execute_algorithm(state)
            
        elif choice == '3':
            display_result(state)
            
        elif choice == '4':
            print("\nЗавершение работы программы. До свидания!")
            sys.exit(0)
            
        else:
            print("Некорректный выбор. Пожалуйста, введите число от 1 до 4.")

if __name__ == "__main__":
    main()