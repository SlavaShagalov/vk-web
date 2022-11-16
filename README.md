# Q&A Platform. Индивидуальный проект по курсу Web-технологии в Технопарке.

## ДЗ 1-3

### Студент: Шагалов Вячеслав WEB-11 (tg: [@slava_shagalov](https://t.me/slava_shagalov))

### Преподаватель: Динар Сабитов

### После клонирования репозитория необходимо сделать следующие действия для инициализации проекта:

- Скачать данные по этой [ссылке](https://disk.yandex.ru/d/OLfS_LngrPZWZg). Поместить файл askme_dump.sql в корневую
  директорию проекта.

- python manage.py init_project (Данная команда скачает и установит docker-образ c СУБД Postgres,
  запустит контейнер, выполнит копирование данных из файла askme_dump.sql в БД и остановит контейнер)
  
- Дальше можно запустить контейнер с СУБД с помощью docker-compose up, запустить сервер с 
помощью python manage.py runserver и тд...

### Админ уже добавлен в askme_dump.sql. Данные для входа в в админку:

- username: admin
- password: 1234

### Пара скриншотов

![image](https://user-images.githubusercontent.com/73226654/202084576-59e2c670-b161-4e5a-89a7-e90be05f45d6.png)

![image](https://user-images.githubusercontent.com/73226654/202084769-0e6e4871-a541-4c41-bedd-944112729553.png)

![image](https://user-images.githubusercontent.com/73226654/202084899-8606b272-118a-43d9-979c-7728598c6137.png)

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

### Загрузка/выгрузка данных БД с помощью Django (медленно)

python manage.py dumpdata > db.json

python manage.py dumpdata --output db.json app

python manage.py loaddata db.json

python manage.py loaddata --app app db.json

### Загрузка данных БД с помощью Postgres (быстро)

docker exec -i askme_db psql --set ON_ERROR_STOP=on --username test_user askme < askme_dump.sql

### Генерация данных для БД

python manage.py fill_db [ratio]
