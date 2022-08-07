[![Yamdb-app workflow](https://github.com/hitrila/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)](https://github.com/hitrila/yamdb_final/actions/workflows/yamdb_workflow.yml)


# Проект: CI и CD проекта api_yamdb в рамках обучения на курсе Python-разработчик Yandex.Practicum.

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий (Category) может быть расширен администратором
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Технологии, используемые на проекте:

>>1. Python ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
>>2. Django ![Django](https://img.shields.io/badge/-Django-0aad48?style=flat-square&logo=Django)
>>3. DjangoRestFramework ![Django Rest Framework](https://img.shields.io/badge/DRF-red?style=flat-square&logo=Django)
>>4. PostgresSQL ![Postgresql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
>>5. Nginx ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat-square&logo=nginx&logoColor=white)
>>6. Swagger ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=flat-square&logo=swagger&logoColor=white)

## Как запустить проект:

В корневом каталоге проекта создайте файл .env  со следующим содержимым:
1. DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
2. DB_NAME=postgres # имя базы данных
3. POSTGRES_USER=postgres # логин для подключения к базе данных
4. POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
5. DB_HOST=db # название сервиса (контейнера)
6. DB_PORT=5432 # порт для подключения к БД 

Скачать docker: 
1. Для [windows](https://docs.docker.com/desktop/windows/install/)
2. Для [macOS](https://docs.docker.com/desktop/mac/install/)
3. Для дистрибутивов [Linux](https://docs.docker.com/desktop/linux/#uninstall)

Из кталога приложения выполнить команду:
```
docker-compose up -d --build
```

Что бы создать суперпользователя, 
необходимо войти в контейнер:

```
docker exec -it id-контейнера bash
```
узнать id-контейнера можно командой 
```
docker container ls
```
Применить миграции:
```
python manage.py migrate
```
Выполнить команду:
```
python manage.py createsuperuser
```
Загрузить дамп базы командой (если требуется):
```
python manage.py loaddata fixtures.json
```
Следующие сервисы будут доступны по адресам:

## API
1. http://localhost:8000/api/swagger/
2. http://localhost:8000/api/redoc/
