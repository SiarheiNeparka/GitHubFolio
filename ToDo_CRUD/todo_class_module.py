"""Модуль, содержащий все необходимые классы и константы, для работы
скрипта."""

import requests
import json
import logging
import configparser
import csv


LOG_FORMAT = "%(asctime)s | Exception occured: %(message)s"
H_CLOSE = {"Connection": "Close"}
H_CONTENT = {"Content-Type": "application/json"}
KEY_NAMES = [
    "id",
    "name",
    "priority",
]
KEY_WIDTHS = [
    10,
    30,
    10,
]


class ToDoConfig:
    """Осуществляет связь с конфигурационным файлом
    todo_config.ini."""

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read("todo_config.ini")


class ToDoLogger:
    """Осуществляет запись исключений, всплывающих во
    время работы программы."""

    def __init__(self) -> None:
        # Создаём логгер с именем '__name__'.
        self.logger = logging.getLogger(__name__)

        # Создаём хэндлер, который будет перезипасывать указанный файл,
        # находящийся в той же директории, что и этот модуль, всякий раз,
        # когда программа будет выполнена.
        self.handler = logging.FileHandler(
            ToDoConfig().config["filename_log"]["file_to_save_log"],
            mode="w",
            encoding="utf-8",
        )

        # Создаём форматтер на основе ранее заданной константы.
        self.formatter = logging.Formatter(LOG_FORMAT)
        # Назначаем форматтер хэндлеру.
        self.handler.setFormatter(self.formatter)

        # Назначаем хэндлер логгеру.
        self.logger.addHandler(self.handler)


class BadIdError(Exception):
    """Обрабатывает исключения, возникающие при создании задачи
    или при обращении к задаче с неверным номером."""

    def __init__(self, message: str, id_: int) -> None:
        super().__init__(message)
        self.id_ = id_


class BadNameError(Exception):
    """Обрабатывает исключения, возникающие при создании пустой,
    или же слишком длинной задачи."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class BadPriorityError(Exception):
    """Обрабатывает исключения, возникающие при создании задачи
    с неверным приоритетом."""

    def __init__(self, message: str, priority: int) -> None:
        super().__init__(message)
        self.priority = priority


class RESTclient:
    """Клиентская часть REST-клиента.

    Атрибуты:
    ---------
    URI: str
        Ссылка для соединения с сервером.

    Методы:
    -------
    show_head(self)
        Выводит на экран шапку итоговой таблицы с задачами.
        Шапка содержит имена столбцов и особое форматирование,
        заданное для отображения списка задач.
    show_task(self, task)
        Выводит на экран строку, содержащую информацию о задаче.
        Строка представляется особым форматированием, присущим для
        данного класса.
    show_tasks(self, json_)
        Выводит на экран задачи, соблюдая заданное форматирование.
        В зависимости от того, какой тип данных поступит в качестве
        передаваемого параметра, метод отработает соответствующим
        образом.
    task_put(self)
        Изменяет введённую ранее задачу.
        Производит все необходимые проверки относительно
        пользовательского ввода.
    task_get(self)
        Отображает запрошенную задачу.
        Производит все необходимые проверки относительно
        пользовательского ввода.
    task_delete(self)
        Удаляет выбранную задачу.
        Производит все необходимые проверки относительно
        пользовательского ввода.
    task_post(self)
        Осуществляет ввод новой задачи в список задач.
        Производит все необходимые проверки относительно
        пользовательского ввода.
    tasks_export_to_csv(self, file)
        Записывает итоговый список задач в csv-файл.
    close_conn(self)
        Посылает get-запрос серверу с указанием закрыть соединение.
    """

    URI = ToDoConfig().config["DEFAULT"]["URI"]

    def show_head(self) -> None:
        """Выводит на экран шапку итоговой таблицы с задачами.

        Шапка содержит имена столбцов и особое форматирование,
        заданное для отображения списка задач.
        """

        for n, w in zip(KEY_NAMES, KEY_WIDTHS):
            print(n.ljust(w), end="| ")
        print()

    def show_task(self, task: dict) -> None:
        """Выводит на экран строку, содержащую информацию о задаче.

        Строка представляется особым форматированием, присущим для
        данного класса.

        Параметры:
        ----------
        task: dict
            Словарь, содержащий номер задачи, ее имя и приоритет.
        """

        for n, w in zip(KEY_NAMES, KEY_WIDTHS):
            print(str(task[n]).ljust(w), end="| ")
        print()

    def show_tasks(self, json_) -> None:
        """Выводит на экран задачи, соблюдая заданное форматирование.

        В зависимости от того, какой тип данных поступит в качестве
        передаваемого параметра, метод отработает соответствующим
        образом.

        Параметры:
        ----------
        json_:
            Список словарей (или словарь), содержащий задачи(-у).
        """

        self.show_head()
        if isinstance(json_, list):
            for task in json_:
                self.show_task(task)
        elif isinstance(json_, dict):
            self.show_task(json_)

    def task_put(self) -> None:
        """Изменяет введённую ранее задачу.

        Производит все необходимые проверки относительно
        пользовательского ввода.
        """

        task_id = int(input("Введите номер задачи: "))

        task_name = input("Введите новую задачу: ")

        if task_name.isspace() or task_name == "":
            raise BadNameError("Ввод пустой строки невозможен.")
        elif len(task_name) > 29:
            raise BadNameError(
                f"Имя задачи слишком велико \
(кол-во символов {len(task_name)} > 29)."
            )

        task_prior = int(input("Введите новый приоритет задачи: "))

        if task_prior not in range(1, 4):
            raise BadPriorityError(
                "Введённое значение д. б. в диапазоне от 1 до 3. Введено:",
                task_prior,
            )

        task = {
            "id": task_id,
            "name": task_name,
            "priority": task_prior,
        }

        try:
            reply = requests.put(
                f'{RESTclient.URI}{task["id"]}',
                headers=H_CONTENT,
                data=json.dumps(task),
            )
        except requests.RequestException:
            raise
        else:
            if reply.status_code == requests.codes.ok:
                try:
                    reply = requests.get(RESTclient.URI)
                except requests.RequestException:
                    raise
                else:
                    if reply.status_code == requests.codes.ok:
                        print()
                        self.show_tasks(reply.json())
            elif reply.status_code == requests.codes.not_found:
                raise BadIdError(
                    "Введенного номера задачи нет в списке. Введено:",
                    task_id,
                )

    def task_get(self) -> None:
        """Отображает запрошенную задачу.

        Производит все необходимые проверки относительно
        пользовательского ввода.
        """

        task_id = input("Введите номер задачи: ")

        try:
            reply = requests.get(
                f"{RESTclient.URI}{task_id}",
            )
        except requests.RequestException:
            raise
        else:
            if reply.status_code == requests.codes.ok:
                print()
                self.show_tasks(reply.json())
            elif reply.status_code == requests.codes.not_found:
                raise BadIdError(
                    "Введенного номера задачи нет в списке. Введено:",
                    task_id,
                )

    def task_delete(self) -> None:
        """Удаляет выбранную задачу.

        Производит все необходимые проверки относительно
        пользовательского ввода.
        """

        task_id = input("Введите номер задачи: ")

        try:
            reply = requests.delete(
                f"{RESTclient.URI}{task_id}",
            )
        except requests.RequestException:
            raise
        else:
            if reply.status_code == requests.codes.ok:
                try:
                    reply = requests.get(RESTclient.URI)
                except requests.RequestException:
                    raise
                else:
                    if reply.status_code == requests.codes.ok:
                        print()
                        self.show_tasks(reply.json())
            elif reply.status_code == requests.codes.not_found:
                raise BadIdError(
                    "Введенного номера задачи нет в списке. Введено:",
                    task_id,
                )

    def task_post(self) -> None:
        """Осуществляет ввод новой задачи в список задач.

        Производит все необходимые проверки относительно
        пользовательского ввода.
        """

        task_id = int(input("Введите номер задачи: "))

        if task_id not in range(1, 16):
            raise BadIdError(
                "Введённый номер д. б. в диапазоне от 1 до 15. Введено:",
                task_id,
            )

        task_name = input("Введите задачу: ")

        if task_name.isspace() or task_name == "":
            raise BadNameError("Ввод пустой строки невозможен.")
        elif len(task_name) > 29:
            raise BadNameError(
                f"Имя задачи слишком велико \
(кол-во символов {len(task_name)} > 29)."
            )

        task_prior = int(input("Введите приоритет задачи: "))

        if task_prior not in range(1, 4):
            raise BadPriorityError(
                "Введённое значение д. б. в диапазоне от 1 до 3. Введено:",
                task_prior,
            )

        new_task = {
            "id": task_id,
            "name": task_name,
            "priority": task_prior,
        }

        try:
            reply = requests.post(
                RESTclient.URI,
                headers=H_CONTENT,
                data=json.dumps(new_task),
            )
        except requests.RequestException:
            raise
        else:
            if reply.status_code == requests.codes.created:
                try:
                    reply = requests.get(RESTclient.URI)
                except requests.RequestException:
                    raise
                else:
                    if reply.status_code == requests.codes.ok:
                        print()
                        self.show_tasks(reply.json())
            elif reply.status_code == requests.codes.server_error:
                raise BadIdError(
                    "Вы ввели номер существующей задачи. Введено:", task_id
                )

    def tasks_export_to_csv(self, file: str) -> None:
        """Записывает итоговый список задач в csv-файл."""

        try:
            reply = requests.get(RESTclient.URI)
        except requests.RequestException:
            raise
        else:
            if reply.status_code == requests.codes.ok:
                try:
                    with open(
                        file,
                        "w",
                        encoding="utf-8",
                        newline="",
                    ) as csvfile:
                        writer_ = csv.DictWriter(
                            csvfile,
                            fieldnames=KEY_NAMES,
                        )

                        writer_.writeheader()
                        for task in reply.json():
                            task_dict = {}
                            for key_name in KEY_NAMES:
                                task_dict.update({key_name: task[key_name]})
                            writer_.writerow(task_dict)
                except IOError:
                    raise

    def close_conn(self) -> None:
        """Посылает get-запрос серверу с указанием закрыть соединение."""

        try:
            reply = requests.get(RESTclient.URI, headers=H_CLOSE)
        except requests.RequestException:
            print("Ошибка связи.")
        else:
            if (
                reply.status_code == requests.codes.ok
                and reply.headers["Connection"] == "close"
            ):
                print("Соединение закрыто.")
            else:
                print("Ошибка сервера.")


if __name__ == "__main__":
    print("todo_class_module.py запущен сам по себе.")
else:
    print("todo_class_module.py импортирован.")
