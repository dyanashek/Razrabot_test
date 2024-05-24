# Tasks API
***
Простой API для управления TODO листом, с покрытием тестами и документацией

## Установка и использование:
- В корне проекта создайте .env, содержащий **DATABASE_URL** (URL для рабочей БД), **TEST_DATABASE_URL** (URL для тестовой БД), в проекте использован MySQL в связке с pymysql
- Установите виртуальное окружение и активируйте его:
> Установка и активация в корневой папке проекта
```sh
python3 -m venv venv
source venv/bin/activate # for macOS
source venv/Scripts/activate # for Windows
```
- Установите зависимости:
```sh
pip install -r requirements.txt
```
- Выполните миграции:
```sh
flask db init
flask db migrate
flask db upgrade
```
- Запустите проект:
```sh
python3 run.py
```
- Документация к API будет доступна по адресу:
http://127.0.0.1:5000/api-docs/
- Для запуска unit тестов (покрытие 99%):
```sh
python3 -m unittest tests/test_tasks.py
```

