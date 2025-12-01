def execute_task_4_algorithm(arr1, arr2, operation='+'):
    # Преобразуем массивы в числа
    num1 = int("".join(map(str, arr1)))
    num2 = int("".join(map(str, arr2)))
    
    if operation == '+':
        res = num1 + num2
    elif operation == '-':
        res = num1 - num2
    else:
        return ["Ошибка"]
    
    # Если отрицательное — добавляем минус
    if res < 0:
        return ['-', *list(map(int, str(-res)))]
    else:
        return list(map(int, str(res)))