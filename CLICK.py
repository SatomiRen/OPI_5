#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import os.path


def get_flight(fls, dest, num, type):
    """
    Добавить данные о работнике.
    """
    fls.append(
        {
            "flight_destination": dest,
            "flight_number": num,
            "airplane_type": type
        }
    )
    return fls


def display_flights(flights):
    """
     Отобразить список рейсов
    """
    if flights:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "No",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолета"
            )
        )
        print(line)
        for idx, flight in enumerate(flights, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:<15} |'.format(
                    idx,
                    flight.get('flight_destination', ''),
                    flight.get('flight_number', ''),
                    flight.get('airplane_type', 0)
                )
            )
        print(line)

    else:
        print("Список рейсов пуст")


def select_flights(flights, airplane_type):
    """
    Выбрать рейсы самолётов заданного типа
    """
    count = 0
    res = []
    for flight in flights:
        if flight.get('airplane_type') == airplane_type:
            count += 1
            res.append(flight)
    if count == 0:
        print("рейсы не найдены")

    return res


def save_flights(file_name, fls):
    """
    Сохранить все записи полётов в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(fls, fout, ensure_ascii=False, indent=4)


def load_flights(file_name):
    """
    Загрузить все записи полётов из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.command()
@click.argument('command')
@click.argument('filename')
@click.option('--flight_dest', prompt='Destination?',
              help='The flight destination'
)
@click.option('--number', prompt='Enter flight num', help='The flight number')
@click.option('--type', prompt='Enter airplane type', help='The airplane type')
def main(command, filename, flight_dest, number, type):
    """
    Главная функция программы
    """
    is_dirty = False
    if os.path.exists(filename):
        flights = load_flights(filename)
    else:
        flights = []
    if command == "add":
        flights = get_flight(
            flights,
            flight_dest,
            number,
            type
        )
        is_dirty = True
    elif command == "display":
        display_flights(flights)
    elif command == "select":
        selected = select_flights(flights, type)
        display_flights(selected)
    if is_dirty:
        save_flights(filename, flights)


if __name__ == '__main__':
    main()
