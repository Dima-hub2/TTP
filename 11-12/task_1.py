def execute_task_1_algorithm(arr1, arr2):
    # Сортируем: первый по убыванию, второй по возрастанию
    a = sorted(arr1, reverse=True)
    b = sorted(arr2)
    
    if len(a) != len(b):
        print("Ошибка: массивы разной длины!")
        return [], [], []
    
    # Считаем с условием: если равны — 0
    result = []
    for i in range(len(a)):
        if a[i] == b[i]:
            result.append(0)
        else:
            result.append(a[i] + b[i])
    
    result = sorted(result)
    return result, a, b