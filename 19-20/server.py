# server.py (простая версия)
import threading
import queue
import time
import random
import logging
from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

# Настройка логирования
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def task1_algorithm(arr1, arr2):
    """Алгоритм задачи 1"""
    a = sorted(arr1, reverse=True)
    b = sorted(arr2)
    
    if len(a) != len(b):
        return [], [], []
    
    result = []
    for i in range(len(a)):
        if a[i] == b[i]:
            result.append(0)
        else:
            result.append(a[i] + b[i])
    
    return sorted(result), a, b

def task4_algorithm(arr1, arr2, operation='+'):
    """Алгоритм задачи 4"""
    num1 = int("".join(map(str, arr1)))
    num2 = int("".join(map(str, arr2)))
    
    if operation == '+':
        res = num1 + num2
    elif operation == '-':
        res = num1 - num2
    else:
        return ["Ошибка"]
    
    if res < 0:
        return ['-', *list(map(int, str(-res)))]
    else:
        return list(map(int, str(res)))

def task5_algorithm(arr, target_sum):
    """Алгоритм задачи 5"""
    arr = list(map(int, arr)) 
    target = int(target_sum)
    count = 0
    n = len(arr)
    
    for i in range(n):
        sum_now = 0
        for j in range(i, n):
            sum_now += arr[j]
            if sum_now == target:
                count += 1
    return count

class TaskServer(threading.Thread):
    """Простой сервер для обработки задач"""
    
    def __init__(self, request_queue):
        super().__init__(daemon=True)
        self.request_queue = request_queue
        self.running = True
        self.processed = 0
        
    def run(self):
        print(f"{ts()} Сервер: запущен")
        print(f"{ts()} Сервер: ожидание запросов...")
        print()
        
        while self.running:
            try:
                # Получаем запрос из очереди
                request = self.request_queue.get(timeout=0.5)
            except queue.Empty:
                continue
            
            client = request.get('client')
            task = request.get('task')
            data = request.get('data')
            callback = request.get('callback')
            
            print(f"{ts()} {client}: получен запрос на {self.task_name(task)}")
            
            # Эмуляция задержки
            delay = random.uniform(1, 3)
            time.sleep(delay)
            
            # Выполняем задачу
            result = None
            try:
                if task == 'task1':
                    result_list, a, b = task1_algorithm(data['arr1'], data['arr2'])
                    result = {
                        'result': result_list,
                        'sorted_arr1': a,
                        'sorted_arr2': b,
                        'success': True
                    }
                elif task == 'task4':
                    operation = data.get('operation', '+')
                    result_list = task4_algorithm(data['arr1'], data['arr2'], operation)
                    result = {
                        'result': result_list,
                        'operation': operation,
                        'success': True
                    }
                elif task == 'task5':
                    count = task5_algorithm(data['arr'], data['target'])
                    result = {
                        'result': count,
                        'success': True
                    }
                else:
                    result = {'success': False, 'error': f"Неизвестная задача: {task}"}
            except Exception as e:
                result = {'success': False, 'error': str(e)}
            
            self.processed += 1
            print(f"{ts()} {client}: выполнена {self.task_name(task)}")
            
            # Отправляем результат
            if callable(callback):
                try:
                    callback(client, task, result, data)
                except:
                    pass
    
    def task_name(self, task_key):
        """Просто возвращает имя задачи"""
        names = {
            'task1': 'обработка массивов',
            'task4': 'арифметика массивов',
            'task5': 'поиск подмассивов'
        }
        return names.get(task_key, task_key)
    
    def stop(self):
        """Просто останавливаем сервер"""
        self.running = False
        print(f"\n{ts()} Сервер: обработано {self.processed} запросов")