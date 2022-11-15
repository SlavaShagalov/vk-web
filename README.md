# Q&A Platform. Индивидуальный проект по курсу Web-технологии в Технопарке.

## ДЗ 1-3

### Студент: Шагалов Вячеслав WEB-11

### Преподаватель: Динар Сабитов

### После клонирования репозитория необходимо выполнить следующие команды из корневой директории для инициализации проекта

source venv/bin/activate

python manage.py init_project

### Что делает init_project

- Выполняет необходимые миграции
- Скачивает докер-образ с Postrges БД, поднимает ее
- Загружает данные из файла с дампом в базу данных
- Создает пользователя admin с паролем 1234

## Полезные команды

### Войти в виртуальное окружение

source venv/bin/activate

### Собрать(--build) и поднять(up) докер контейнер с postgres СУБД в фоновом режиме(-d)

docker-compose up -d --build

### Остановить докер контейнер с postgres СУБД

docker-compose stop

### Миграции

python manage.py migrate

python manage.py makemigrations app

python manage.py sqlmigrate app 0001

python manage.py shell

### Создать админа

python manage.py createsuperuser

### Создать requirements.txt

pip freeze > requirements.txt

### Загрузка/выгрузка данных БД

python manage.py dumpdata > db.json

python manage.py dumpdata --output db.json app

python manage.py loaddata db.json

python manage.py loaddata --app app db.json

### Postrges load from dump file

docker exec -i askme_db psql --set ON_ERROR_STOP=on --username test_user askme < askme_dump.sql

### Генерация данных для БД

python manage.py fill_db [ratio]
