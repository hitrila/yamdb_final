Групповой проект в рамках учебного проекта Yandex.Practicum.
=
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles).\
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».\
Список категорий (Category) может быть расширен администратором\
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).\
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

>Технологии, используемые на проекте:

>Backend:
>>1. Python ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
>>2. Django ![Django](https://img.shields.io/badge/-Django-0aad48?style=flat-square&logo=Django)
>>3. DjangoRestFramework ![Django Rest Framework](https://img.shields.io/badge/DRF-red?style=flat-square&logo=Django)


Как запустить проект:
=
>Способ номер 1:

На проекты мы используем почтовый сервис [SendGrid](https://sendgrid.com/).\
Пример с настройкой сервиса [тут](https://pythonru.com/primery/otpravka-pisem-s-formy-v-django)

В корневую папку проекта расположить .env файл со следующими параметрами:
1. SECRET_KEY=***ВАШ СЕКРЕТНЫЙ КЛЮЧ***
2. EMAIL_HOST_PASSWORD=***Секретный ключ от почты***
3. RECIPIENTS_EMAIL=***ЭЛ.АДРЕСА ПОЛУЧАТЕЛЕЙ***
4. DEFAULT_FROM_EMAIL=***ПОЧТА ОТПРАВИТЕЛЯ***

Выполнять стандартные команды для запуска проекта
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
При необходимости залить тестовые данные из CSV файлов командой:
```
python manage.py load_csv
```
>Способ номер 2:

В корневую папку проекта расположить .env файл со следующими параметрами:
На проекты мы используем почтовый сервис [SendGrid](https://sendgrid.com/).\
Пример с настройкой сервиса [тут](https://pythonru.com/primery/otpravka-pisem-s-formy-v-django)

:exclamation: ВНИМАНИE! Следует выполнять сборку и запуск только в режиме <br> Debug=False :exclamation:

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

После установки проверьте конфигурацию переменных окружений\
командой:
```
docker-compose config
```
Если всё успешно, все переменные на местах, запустить командой:
```
docker-compose up --build
```

Что бы создать суперпользователя, \
необходимо войти в контейнер командой:
```
docker exec -it drf_backend bash
```
Перейти в каталог api:
```
cd api_yamdb
```
После ввести команду:
```
python manage.py createsuperuser
```
и следовать дальнейшим инструкциям.

При необходимости залить тестовые данные из CSV файлов командой:
```
python manage.py load_csv
```
Для выхода введите:
```
exit
```
Теперь, благодаря использованию Nginx нет необходимости прописывать порт.
Следующие сервисы будут доступны по адресам:
```
API
http://localhost/api/swagger/
http://localhost/api/redoc/
```
```
UI панель базы данный PostgeSQL
http://localhost/pgadmin4/
```
Так же сервисы будут доступны в вашей локальной сети.
:exclamation: ВНИМАНИE! Следует выполнять сборку и запуск только в режиме <br> Debug=False :exclamation:

Как приступить к работе:
=
Создать свою ветку командой:
```
git branch "имя ветки"
```
Перейти на ветку командой:
```
git checkout "имя ветки"
```
Приступить к разработке новой фичи!:muscle:

Как правильно запушить проект.
=
1. Проверить python style линтером black. Выполнить команду ***black .***
2. Проверить PEP8. Выполнить команду ***flake8***. В случае ошибок, исправить и повторить пункт 1.
3. Тесты. Тесты будем запускать уже на финишней прямой, так как они проверяют целиком весь проект. Но ничего не мешает найти в папке tests необходимый вам файл и запустить его. Так же можно написать свои тесты. :muscle: 

Участники проекта:
1. [Оболихин Федор](https://github.com/GideonRavenor1)
2. [Павел Жиляков](https://github.com/Destrifer)
3. [Дарвишев Иннокентий](https://github.com/hitrila)

Ревью проводит:
1. Юрий Никулин.

Наставник:
1. [Киреев Юрий](https://github.com/kireevys)

Диаграмма БД:\
[Кликать тут](https://dbdiagram.io/d/6268201595e7f23c6178c6cc)
