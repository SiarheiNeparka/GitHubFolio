# ToDo List
## _RESTful планер (насколько это возможно)_

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

ToDo List это приложение, представляющее клиентскую часть работы с сервером, хранящим список задач пользователя.

- Выберите нужный пункт в меню.
- Следуйте дальнейшим инструкциям по работе со списком задач.
- Повышайте свою продуктивность!

## Функции

- Создавайте новые задачи.
- Редактируйте ранее созданные задачи.
- Удаляйте ненужные более задачи.
- Обращайтесь к нужным задачам для их просмотра.
- Экспортируйте ваш список задач в csv-файл.


ToDo List это приложение, позволяющее вам создавать до 15 задач и наделять их приоритетами: от самых важных задач (1 приоритет), до менее срочных и важных дел (3 приоритет).

## Технология

ToDo List использует следующие сторонние модули:

- requests - is an HTTP library, written in Python.
- json - JavaScript Object Notation is a subset of JavaScript syntax (ECMA-262 3rd edition) used as a lightweight data interchange format. json exposes an API familiar to users of the standard library
marshal and pickle modules.
- logging - logging package for Python. Based on PEP 282 and comments thereto in comp.lang.python.
- configparser - configuration file parser.
- csv - read/write/investigate CSV files.
- os - OS routines for NT or Posix depending on what system we're on.

## Установка

Для запуска серверной части приложения вам потребуется [Node.js](https://nodejs.org/).

Если у вас отсутствует json-server, то пропишите в вашей консоли следующую команду и дождитесь завершения установки:

```sh
npm install -g json-server
```

После успешного завершения установки вы будете готовы запустить сервер для работы ToDo List'a. Укажите в консоли путь до папки с программой, после чего пропишите следующую команду:

```sh
json-server --watch tasks.json
```

Сервер успешно запущен. Давайте запустим клиентскую часть программы. 

В новой командной строке укажите путь до папки с программой и пропишите следующую строку:

```sh
py main.py
```

Следуйте инструкциям на экране.

### Enjoy!
