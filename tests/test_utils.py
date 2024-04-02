import os

import pytest

from config import ROOT_DIR
from src.utils import creating_list_operations
from src.utils import get_data
from src.utils import get_hide_number
from src.utils import load_json


def test_get_data():
    """
    Проверяем формат даты
    """
    assert get_data('2019-04-19T12:02:30.129240') == '19.04.2019'
    assert get_data('2018-02-13T04:43:11.374324') == '13.02.2018'


def test_get_hide_number():
    """
    Проверяем скрытие номера счета и карты
    """
    assert get_hide_number('Счет 33355011456314142963') == 'Счет **2963'
    assert get_hide_number('Карта VISA 1111222233334444') == 'Карта VISA 1111 22** **** 4444'
    assert get_hide_number('Карта Visa Platinum 1813166339376336') == 'Карта Visa Platinum 1813 16** **** 6336'


@pytest.fixture
def mock_json_data():
    return [{}]


def test1_creating_list_operations(capsys, mock_json_data):
    """
    Проверяем ОТКРЫТИЕ ВКЛАДА
    :param capsys:
    :param mock_json_data:
    :return:
    """
    mock_json_data = [
        {
            "id": 596171168,
            "state": "EXECUTED",
            "date": "2018-07-11T02:26:18.671407",
            "operationAmount": {
                "amount": "79931.03",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 72082042523231456215"
        },
    ]
    creating_list_operations(mock_json_data, operation_counter=5)

    captured = capsys.readouterr()  # Считываем вывод консоли
    assert '11.07.2018 Открытие вклада' in captured.out  # Проверяем вывод даты
    assert 'Счет **6215' in captured.out  # Проверяем вывод описания операции
    assert '79931.03 руб.' in captured.out  # Проверяем вывод суммы операции


def test2_creating_list_operations(capsys, mock_json_data):
    """
    Проверяем ПЕРЕВОД ОРГАНИЗАЦИИ
    """
    mock_json_data = [
        {
            "id": 716496732,
            "state": "EXECUTED",
            "date": "2018-04-04T17:33:34.701093",
            "operationAmount": {
                "amount": "40701.91",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Gold 5999414228426353",
            "to": "Счет 72731966109147704472"
        },
    ]
    creating_list_operations(mock_json_data, operation_counter=5)

    captured = capsys.readouterr()
    assert '04.04.2018 Перевод организации' in captured.out  # Проверяем вывод даты
    assert 'Visa Gold 5999 41** **** 6353 -> Счет **4472' in captured.out  # Проверяем вывод описания операции
    assert '40701.91 USD' in captured.out  # Проверяем вывод суммы операции


def test3_creating_list_operations(capsys, mock_json_data):
    """
    Проверяем окончание счетчика операций
    """
    mock_json_data = [
        {
            "id": 716496732,
            "state": "EXECUTED",
            "date": "2018-04-04T17:33:34.701093",
            "operationAmount": {
                "amount": "40701.91",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Gold 5999414228426353",
            "to": "Счет 72731966109147704472"
        },
    ]
    creating_list_operations(mock_json_data, operation_counter=0)

    captured = capsys.readouterr()
    assert '' in captured.out  # Проверяем вывод даты


def test_load_json():
    """
    Проверяем загрузку json файла
    """
    TEST_DATA_PATH = os.path.join(ROOT_DIR, 'tests', 'test.json')
    assert load_json(TEST_DATA_PATH) == [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        }]
