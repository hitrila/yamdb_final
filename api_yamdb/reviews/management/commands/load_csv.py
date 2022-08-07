import csv
import os
from typing import List, Union, Sequence

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import connection, IntegrityError

User = get_user_model()


class Command(BaseCommand):
    """
    Команда для загрузки данных в БД.
    В случае ошибки при записи, будет инициализированная повторная
    попытка записи.
    """

    help = 'Загрузка данных и CSV файлов'
    retry_requests_dictionary = {}
    SUCCESS_MESSAGE = 'УСПЕШНО'
    PATH_TO_FILES = '../api_yamdb/static/data'

    # Добавьте в словарь TABLES имя файла без расширения .csv
    # и имя таблицы. Ключ - имя файла, значение - имя таблицы.
    # НЕ ЗАБУДЬТЕ ПРО ПРЕФИКС "ИМЯ ПРИЛОЖЕНИЯ_ИМЯ ТАБЛИЦЫ",
    # если ясно не указывали имена таблиц.

    TABLES = {
        'users': 'reviews_user',
        'category': 'reviews_category',
        'titles': 'reviews_title',
        'genre': 'reviews_genre',
        'genre_title': 'reviews_title_genre',
        'comments': 'reviews_comment',
        'review': 'reviews_review',
    }

    def handle(
        self,
        *args,
        **options,
    ):
        list_files = os.listdir(self.PATH_TO_FILES)
        with connection.cursor() as cursor:
            for file in list_files:
                with open(
                    self.PATH_TO_FILES + '/' + file, 'r', encoding='utf-8'
                ) as csv_file:
                    file_name = file.split('.')[0]
                    table = self.TABLES.get(file_name)
                    csv_reader = csv.DictReader(csv_file)

                    if table is None:
                        error = self.get_error_message(
                            name='UNKNOWN_TABLE',
                            table_name=file_name,
                        )
                        self.stdout.write(self.style.ERROR(error))
                        continue

                    # Из-за множества полей в таблицы пользователей по
                    # умолчанию, дешевле было в данном случае использовать ORM.
                    if file_name == 'users':
                        self.create_users(table=table, csv_reader=csv_reader)
                        continue

                    keys = list(csv_reader.fieldnames)
                    values = [
                        f'{(*self.substitute_quotes(list(element.values())),)}'
                        for element in list(csv_reader)
                    ]
                    raw_queries = self.get_raw(
                        table=table,
                        columns=keys,
                        values=values,
                    )
                    result = self.execute_raw(
                        raw_queries=raw_queries,
                        table=table,
                        cursor=cursor,
                    )
                    if result == self.SUCCESS_MESSAGE:
                        self.stdout.write(self.style.SUCCESS(result))
                    else:
                        self.stdout.write(self.style.ERROR(result))

                        # Если произошла ошибка во время записи, raw_queries
                        # добавятся в словарь повторного запуска.
                        self.add_raw_queries_to_retry_dict(
                            table=table,
                            raw_queries=raw_queries,
                        )
                        self.stdout.write(
                            'Добавление '
                            f'raw_queries {table} '
                            'в повторную попытку записи.'
                        )

            # Повторная попытка записи в случае наличия элементов в словаре.

            if self.retry_requests_dictionary:
                message = '=' * 20 + ' ПОВТОРНАЯ ПОПЫТКА ЗАПИСИ ' + '=' * 20
                self.stdout.write(self.style.WARNING(message))
                self.retry_execute_raw(cursor=cursor)
            self.stdout.write(self.style.SUCCESS('ЗАВЕРШЕНИЕ ОПЕРАЦИИ'))

    def execute_raw(
        self,
        raw_queries: str,
        table: str,
        cursor: connection,
    ) -> str:
        """
        Загрузка файлов в БД.
        :param raw_queries: Сырые запросы в формате строки.
        :param table: Имя таблицы.
        :param cursor: Курсор.
        :return: Успешный ответ или raw_queries.
        """

        try:
            cursor.execute(raw_queries)
            result = self.SUCCESS_MESSAGE
        except IntegrityError as Error:
            if 'FOREIGN KEY' in str(Error):
                result = self.get_error_message(
                    name='RELATION_ERROR',
                    table_name=table,
                )
            else:
                result = self.get_error_message(
                    name='UNIQUE_ERROR',
                    table_name=table,
                )

        return result

    def retry_execute_raw(
        self,
        cursor: connection,
    ) -> None:
        """
        Функции повторной записи в БД.
        :param cursor: Курсор.
        :return: None
        """

        for key, value in self.retry_requests_dictionary.items():
            for raw_queries in value:
                result = self.execute_raw(
                    raw_queries=raw_queries,
                    cursor=cursor,
                    table=key,
                )
                if result == self.SUCCESS_MESSAGE:
                    self.stdout.write(self.style.SUCCESS(result))
                else:
                    self.stdout.write(self.style.ERROR(result))

    @staticmethod
    def get_error_message(
        name: str,
        table_name: str,
    ) -> str:
        """
        Получение ошибки по ключу.
        :param name: Имя ошибки.
        :param table_name: Имя таблицы.
        :return: Ошибка в формате строки.
        """

        errors = {
            'UNKNOWN_TABLE': (
                'Ошибка при загрузке данных. '
                f'Таблица {table_name} отсутствует в словаре TABLES'
            ),
            'RELATION_ERROR': (
                'Ошибка при загрузке данных '
                f'в таблицу {table_name}. '
                'Одно из отношений еще не создано.'
            ),
            'UNIQUE_ERROR': (
                'Ошибка при загрузке данных '
                f'в таблицу {table_name}. '
                'Запись в таблице уже существует'
            ),
        }
        return errors[name]

    @staticmethod
    def get_raw(
        table: str,
        columns: List[str],
        values: List[Union[int, str]],
    ) -> str:
        """
        Получить сырой запрос.
        :param table: Имя таблицы.
        :param columns: Имена столбцов
        :param values: Значение столбцов.
        :return: Сырой запрос в формате строки.
        """

        raw_queries = (
            "INSERT INTO {table} ({columns}) VALUES  {values}"
        ).format(
            table=table, columns=', '.join(columns), values=', '.join(values)
        )
        return raw_queries

    def add_raw_queries_to_retry_dict(
        self,
        table: str,
        raw_queries: str,
    ) -> None:
        """
        Добавление raw_queries в словарь на повторную запись.
        :param table: Имя таблицы.
        :param raw_queries: Сырые запросы.
        :return: None
        """

        if table not in self.retry_requests_dictionary:
            self.retry_requests_dictionary[table] = []
            self.retry_requests_dictionary[table].append(raw_queries)
        else:
            self.retry_requests_dictionary[table].append(raw_queries)

    def create_users(self, table: str, csv_reader: csv.DictReader) -> None:
        """
        Метод создания пользователей.
        :param table: Имя таблицы.
        :param csv_reader: Парсер с данными из файла.
        :return: None
        """

        try:
            users = [User(**data) for data in csv_reader]
            User.objects.bulk_create(users)
            self.stdout.write(self.style.SUCCESS(self.SUCCESS_MESSAGE))
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(
                    self.get_error_message(
                        name='UNIQUE_ERROR',
                        table_name=table,
                    )
                )
            )

    @staticmethod
    def substitute_quotes(
        data: Union[Sequence[Union[int, str]]]
    ) -> Union[list[str], str]:
        """
        Функция форматирования списка/кортежа значений, либо отдельного
        элемента,
        под валидные ковычки для sql row.
        :param data: Последовательность или отдельный элемент.
        :return: Последовательность или отдельный элемент.
        """
        result = [
            int(value) if value.isdigit() else f'{value}' for value in data
        ]
        return result
