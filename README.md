[![Yamdb-app workflow](https://github.com/GideonRavenor1/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/GideonRavenor1/yamdb_final/actions/workflows/yamdb_workflow.yml)

# Учебный проект YaMDb в рамках учебы Yandex.Practicum.

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен администратором
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

>Технологии, используемые на проекте:

>Backend:
>>1. Python ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
>>2. Django ![Django](https://img.shields.io/badge/-Django-0aad48?style=flat-square&logo=Django)
>>3. DjangoRestFramework ![Django Rest Framework](https://img.shields.io/badge/DRF-red?style=flat-square&logo=Django)
>>4. PostgresSQL ![Postgresql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
>>5. pgAdmin ![pgAdmin](https://img.shields.io/badge/PG-pgAdmin-blue?style=flat-square&logo=pgAdmin)
>>6. Nginx ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat-square&logo=nginx&logoColor=white)
>>7. Swagger ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=flat-square&logo=swagger&logoColor=white)

# Как запустить проект:

На проекты мы используем почтовый сервис [SendGrid](https://sendgrid.com/).\
Пример с настройкой сервиса [тут](https://pythonru.com/primery/otpravka-pisem-s-formy-v-django)

На проекты мы используем почтовый сервис [SendGrid](https://sendgrid.com/).\
Пример с настройкой сервиса [тут](https://pythonru.com/primery/otpravka-pisem-s-formy-v-django)

В папку ***infra*** расположить .env файл со следующими параметрами:
1. SECRET_KEY=***ВАШ СЕКРЕТНЫЙ КЛЮЧ***
2. EMAIL_HOST_PASSWORD=***СЕКРЕТНЫЙ КЛЮЧ ОТ ПОЧТЫ***
3. RECIPIENTS_EMAIL=***ЭЛ.АДРЕСА ПОЛУЧАТЕЛЕЙ***
4. DEFAULT_FROM_EMAIL=***ПОЧТА ОТПРАВИТЕЛЯ***
5. NAME=***ВАША БАЗА ДАННЫХ***
6. USER=***ВАШЕ ИМЯ ПОЛЬЗОВАТЕЛЯ***
7. PASSWORD=***ВАШ ПАРОЛЬ***
8. HOST=***ХОСТ, УКАЗАТЬ СЛУЖБУ БД,В НАШЕМ СЛУЧАЕ postgresql_db***
9. PORT=***ПОРТ, ПО УМОЛЧАНИЮ 5432***
10. PGADMIN_DEFAULT_EMAIL=***ВАША ПОЧТА***
11. PGADMIN_DEFAULT_PASSWORD=***ВАШ ПАРОЛЬ***

Скачать docker: 
1. Для [windows](https://docs.docker.com/desktop/windows/install/)
2. Для [macOS](https://docs.docker.com/desktop/mac/install/)
3. Для дистрибутивов [Linux](https://docs.docker.com/desktop/linux/#uninstall)

После установки проверьте конфигурацию переменных окружений 
командой:
```
docker-compose config
```
Если всё успешно, все переменные на местах, запустить командой:
```
docker-compose -f docker-compose.dev.yml up --build -d
```

Что бы создать суперпользователя, 
необходимо войти в контейнер командой:
```
docker exec -it drf_backend bash
```
Применить миграции:
```
python manage.py migrate
```
После ввести команду:
```
python manage.py createsuperuser
```
и следовать дальнейшим инструкциям.
```
Загрузить дамп базы командой:
```
python manage.py loaddata fixtures/fixtures.json
```
Для выхода введите:
```
exit
```
Следующие сервисы будут доступны по адресам:

## API
1. http://localhost:8000/api/swagger/
2. http://localhost:8000/api/redoc/

## UI панель базы данный PostgeSQL
1. http://localhost:5050


## Развернутый экземпляр приложения доступен по адресу:
## API
1. http://yatube-yandex.ddns.net/api/swagger/
2. http://yatube-yandex.ddns.net/api/redoc/

## UI панель базы данный PostgeSQL
1. http://yatube-yandex.ddns.net/pgadmin4/