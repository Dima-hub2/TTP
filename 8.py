# Итерация 1: все основные функции — заглушки

def show_menu():
    return "меню показано (заглушка)"

def input_data():
    return "данные введены (заглушка)"

def run_algorithm():
    return "алгоритм выполнен (заглушка)"

def show_result():
    return "результат показан (заглушка)"

def main():
    while True:
        print(show_menu())
        choice = input("Выбор: ")
        if choice == "1":
            print(input_data())
        elif choice == "2":
            print(run_algorithm())
        elif choice == "3":
            print(show_result())
        elif choice == "0":
            print("Выход")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()