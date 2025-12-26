# client.py (простая версия)
import threading
import time
import random
from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

class ClientThread(threading.Thread):
    """Простой клиент"""
    
    def __init__(self, name, request_queue, actions):
        super().__init__(daemon=True)
        self.name = name
        self.request_queue = request_queue
        self.actions = actions
        self.results = []
    
    def run(self):
        print(f"{ts()} {self.name}: клиент запущен")
        time.sleep(0.1)
        
        for action in self.actions:
            task = action['task']
            
            # Генерируем данные если нужно
            if action.get('generate', False):
                data = self.generate_data(task)
                self.print_generated(task, data)
            else:
                data = action.get('data', {})
            
            # Отправляем запрос
            print(f"{ts()} {self.name}: отправлен запрос на {self.task_name(task)}")
            
            request = {
                'client': self.name,
                'task': task,
                'data': data,
                'callback': self.callback
            }
            self.request_queue.put(request)
            
            # Ждем перед следующим запросом
            time.sleep(random.uniform(0.2, 0.9))
        
        print(f"{ts()} {self.name}: выполнение завершено")
    
    def generate_data(self, task):
        """Просто генерирует данные для задачи"""
        if task == 'task1':
            size = random.randint(3, 8)
            return {
                'arr1': [random.randint(-10, 10) for _ in range(size)],
                'arr2': [random.randint(-10, 10) for _ in range(size)]
            }
        elif task == 'task4':
            len_a = random.randint(2, 4)
            len_b = random.randint(2, 4)
            return {
                'arr1': [random.randint(0, 9) for _ in range(len_a)],
                'arr2': [random.randint(0, 9) for _ in range(len_b)],
                'operation': random.choice(['+', '-'])
            }
        elif task == 'task5':
            size = random.randint(5, 10)
            return {
                'arr': [random.randint(-5, 5) for _ in range(size)],
                'target': random.randint(-10, 10)
            }
        return {}
    
    def print_generated(self, task, data):
        """Просто выводит что сгенерировали"""
        if task == 'task1':
            print(f"  Массивы: {data['arr1']} и {data['arr2']}")
        elif task == 'task4':
            print(f"  Числа: {data['arr1']} и {data['arr2']}, операция: {data['operation']}")
        elif task == 'task5':
            print(f"  Массив: {data['arr']}, сумма: {data['target']}")
        print()
    
    def callback(self, client_name, task, result, input_data):
        """callback для получения результатов"""
        print(f"{ts()} {self.name}: получен результат")
        
        if not result.get('success', False):
            print(f"  Ошибка: {result.get('error', '?')}")
            print()
            return
        
        if task == 'task1':
            print(f"  Результат: {result['result']}")
        elif task == 'task4':
            arr1 = ''.join(map(str, input_data['arr1']))
            arr2 = ''.join(map(str, input_data['arr2']))
            op = input_data.get('operation', '+')
            res = result['result']
            print(f"  {arr1} {op} {arr2} = {res}")
        elif task == 'task5':
            print(f"  Найдено подмассивов: {result['result']}")
        print()
        
        self.results.append((task, result))
    
    def task_name(self, task_key):
        """Просто возвращает имя задачи"""
        names = {
            'task1': 'обработка массивов',
            'task4': 'арифметика массивов',
            'task5': 'поиск подмассивов'
        }
        return names.get(task_key, task_key)