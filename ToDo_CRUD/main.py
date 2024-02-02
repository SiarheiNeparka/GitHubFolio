"""Модуль, объединяющий в себе оформление скрипта и его функционал.

Формирует пользовательское меню скрипта.
"""

from todo_class_module import (
    RESTclient,
    ToDoLogger,
    BadIdError,
    BadNameError,
    BadPriorityError,
    ToDoConfig,
)
from main_menu_module import (
    main_menu,
    inf,
    INTRO,
)
import requests
from os import strerror


def main() -> None:
    """Запускает программу "ToDo list".

    Программа позволяет ввести до 15 задач с установкой их приоритетов
    и формирует из них итоговый список, который впоследствии можно
    экспортировать в json-файл.
    Логика программы завязана на связи с сервером посредством HTTP-методов.
    """

    print(INTRO)
    inf()

    main_menu()

    to_do_log = ToDoLogger()

    what_to_do = input("\nВведите номер необходимой вам операции: ")

    while what_to_do != "0":
        if what_to_do == "1":
            try:
                RESTclient().task_put()
            except BadIdError as bide:
                to_do_log.logger.critical(f"{bide} {bide.id_}")
                print("Ошибка. Проверьте todo.log.")
            except BadNameError as bne:
                to_do_log.logger.critical(bne)
                print("Запись задачи не удалась. Проверьте todo.log.")
            except BadPriorityError as bpe:
                to_do_log.logger.critical(f"{bpe} {bpe.priority}")
                print("Запись задачи не удалась. Проверьте todo.log.")
            except ValueError:
                to_do_log.logger.critical(
                    "Введённые вами данные некорректны.",
                )
                print("Ошибка. Проверьте todo.log.")
            except requests.RequestException:
                to_do_log.logger.critical("Ошибка связи.")
                print("Ошибка. Проверьте todo.log.")
            else:
                print("Задача успешно изменена.")
        elif what_to_do == "2":
            try:
                RESTclient().task_get()
            except BadIdError as bide:
                to_do_log.logger.critical(f"{bide} {bide.id_}")
                print("Ошибка. Проверьте todo.log.")
            except requests.RequestException:
                to_do_log.logger.critical("Ошибка связи.")
                print("Ошибка. Проверьте todo.log.")
        elif what_to_do == "3":
            try:
                RESTclient().task_delete()
            except BadIdError as bide:
                to_do_log.logger.critical(f"{bide} {bide.id_}")
                print("Ошибка. Проверьте todo.log.")
            except requests.RequestException:
                to_do_log.logger.critical("Ошибка связи.")
                print("Ошибка. Проверьте todo.log.")
            else:
                print("Задача успешно удалена.")
        elif what_to_do == "4":
            try:
                RESTclient().task_post()
            except BadIdError as bide:
                to_do_log.logger.critical(f"{bide} {bide.id_}")
                print("Запись задачи не удалась. Проверьте todo.log.")
            except BadNameError as bne:
                to_do_log.logger.critical(bne)
                print("Запись задачи не удалась. Проверьте todo.log.")
            except BadPriorityError as bpe:
                to_do_log.logger.critical(f"{bpe} {bpe.priority}")
                print("Запись задачи не удалась. Проверьте todo.log.")
            except ValueError:
                to_do_log.logger.critical("Введённые вами данные некорректны.")
                print("Запись задачи не удалась. Проверьте todo.log.")
            except requests.RequestException:
                to_do_log.logger.critical("Ошибка связи.")
                print("Ошибка. Проверьте todo.log.")
            else:
                print("Задача успешно добавлена в список.")
        elif what_to_do == "5":
            try:
                RESTclient().tasks_export_to_csv(
                    ToDoConfig().config["filename_csv"]["file_to_save_csv"]
                )
            except requests.RequestException:
                to_do_log.logger.critical("Ошибка связи.")
                print("Ошибка. Проверьте todo.log.")
            except IOError as ioe:
                to_do_log.logger.critical(strerror(ioe.errno))
                print("Ошибка. Проверьте todo.log.")
            else:
                print("Файл успешно записан.")
        elif what_to_do == "9":
            inf()
        else:
            print(
                f'Введенной операции ("{what_to_do}") ',
                "не существует. Повторите ввод.",
            )

        print()
        main_menu()

        what_to_do = input("\nВведите номер необходимой вам операции: ")

    RESTclient().close_conn()
    print("\nДо встречи!")


if __name__ == "__main__":
    print(
        "main.py запущен сам по себе",
        "как самостоятельный модуль (программа).\n",
    )
    main()
else:
    print(
        "main.py запущен не сам по себе,",
        "а как встраиваемый модуль в другую программу.\n",
    )
