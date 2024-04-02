import json
from datetime import datetime


def load_json(file_name='operations.json'):
    """
    Загрузка файл со списком операций, совершенных клиентом банка
    """
    with open(file_name, 'r', encoding='utf-8') as open_file:
        json_data = json.load(open_file)
    return json_data


def creating_list_operations(json_data, operation_counter=5):  # Количество последних операции
    """Создание списка из словарей с информацией об операциях и вывод на экран"""

    # Фильтрация по выполненным операциям и отсечение пустых словарей
    json_adjective = list(filter(lambda x: len(x) and x['state'] == 'EXECUTED', json_data))

    # Сортировка по дате
    json_sort = sorted(json_adjective, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%dT%H:%M:%S.%f"), reverse=True)

    for operation in json_sort:  # Перебор словарей с операциями
        if operation_counter == 0:  # Проверка на количество операций
            break  # Выход из цикла
        print(get_data(operation['date']), operation['description'])  # Вывод даты и описания операции
        if operation['description'] != 'Открытие вклада':  # Проверка на открытие вклада
            print(get_hide_number(operation['from']) + ' -> ', end='')  # Вывод скрытого номера счета
        print(get_hide_number(operation['to']))  # Вывод скрытого номера счета или карты
        # Вывод суммы и валюты
        print(operation['operationAmount']['amount'], operation['operationAmount']['currency']['name'], '\n')
        operation_counter -= 1  # Уменьшение счетчика последних операций




def get_hide_number(s):
    """
    Принимает строку с номером счета или карты
    возвращает скрытый номер счета или карты
    """
    tmp = s.split()  # Разделение строки по пробелам
    if tmp[0] == 'Счет':
        # Формирование скрытого номера счета
        return f"Счет **{s[-4:]}"
    else:
        card_name = ' '.join(tmp[:-1])  # Формирование названия карты
        # Формирование скрытого номера карты
        return f"{card_name} {tmp[-1][:4]} {tmp[-1][4:6]}** **** {tmp[-1][-4:]}"


def get_data(s):
    """Получает дату из строки в формате DD.MM.YYYY"""
    return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')


def main():
    """Основная функция приложения"""
    creating_list_operations(load_json())