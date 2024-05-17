# Music shop

### Магазин музыкальных инструментов


## Описание

Это пэт-проект, целью которого является перевод существующего магазина 
музыкальных инструментов с WordPress на DRF, написание API и фронтэнда 
магазина (фронтэнд в стадии разработки).

## Возможности:
- Размещение товаров (описание, характеристики, изображение и т.д.) 
через админ-панель,
- Создание категорий, тегов и их присваивание отдельным товарам,
- Возможность редактировать "видимость" товара в каталоге с помощью опции 
"Опубликовано?" в разделе редактирования товара,
- Возможность размещать товар как участвующий в распродаже с соответствующей 
ценой, отличающейся от основной цены,
- Создание записей в блоге с помощью интегрированного TinyMCE редактора,
- Изменение видимости записей в блоке с помощью опции "Опубликовано?" 
в разделе редактирования записи,
- Возможность поиска товара по названию,
- Возможность сортировать товары по полной стоимости (от минимальной 
к максимальной и наоборот) и по цене по распродаже (от минимальной к 
максимальной и наоборот),
- Возможность фильтровать товары (по тегу, по нескольким тегам, по участию 
в распродаже, по факту пометки уникальным предложением)
- Каждый заказ имеет уникальный десятизначный идентификатор,
- Для покупки не нужна учетная запись в магазине, корзина хранится в сессии,
- При заказе отправляется письмо администратору и покупателю с информацией о 
заказе,
- При изменении статуса заказа покупателю отправляется письмо с измененным 
статусом,
- Возможность импортировать и экспортировать теги, категории, товары 
(без изображений), импортировать заказы.

## Стек технологий:
* celery==5.3.6
* Django==4.2.11
* djangorestframework==3.15.1
* django-import-export==3.3.8
* flower==2.0.1
* redis==5.0.3


## Запуск проекта

<details>

<summary>Инструкция по запуску в режиме локальной разработки</summary>

### **_Запуск из консоли._**

Клонируйте репозиторий с **develop веткой** к себе на машину:
```
git clone git@github.com:trsv-dev/music_shop.git -b develop
```
Перейдите в папку проекта:
```
cd music_shop/
```
Установите виртуальное окружение (**если работаете в Linux**):
```
python3.12 -m venv venv
```
Активируйте виртуальное окружение:
```
source venv/bin/activate
```
Перейдите в папку **backend**:
```
cd backend/
```
Переименовать **.env.example** в **.env**.

Убедитесь, что конфигурация Celery в .env настроена на использование в локальной среде.
Она должна выглядеть так:
```
#Celery settings:
###############################################################################

#### Uncomment these two strings if you use it in Docker:
#### Comment it if you use in in local development:
#CELERY_BROKER_URL='redis://redis:6379/0'
#CELERY_RESULT_BACKEND='redis://redis:6379/0'

#### Uncomment these two strings if you use in in local development.
#### Comment it if you use Docker:
CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0'

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
```
Чтобы работало оповещение покупателя и админа о новом заказе, 
в .env замените раздел с email на тестовые настройки (используйте свой почтовый 
аккаунт, т.к. тестовый аккаунт может перестать работать):
```
#Email settings:
###############################################################################
RECIPIENT_ADDRESS='trsv.dev@yandex.ru'
EMAIL_HOST='smtp.yandex.ru'
EMAIL_PORT=465
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL='trsv.dev@yandex.ru'
EMAIL_HOST_USER='trsv.dev@yandex.ru'
EMAIL_HOST_PASSWORD='hzitlzdryltagtly'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
```
и укажите email администратора (замените на свой):
```
ADMIN_EMAIL=admin@email.xoxo
```
Убедитесь, что в **/backend/music_shop/settings.py** в качестве базы данных 
используется SQLite, а не PostgreSQL. Секция с настройками баз данных должна 
выглядеть так:
```
# SQLite's settings (for local development):
###############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL's settings (for production or locally in containers):
###############################################################################

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('POSTGRES_DB', 'django'),
#        'USER': os.getenv('POSTGRES_USER', 'django'),
#        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'you_need_to_set_the_password_in_env'),
#        'HOST': os.getenv('DB_HOST', 'localhost'),
#        'PORT': os.getenv('DB_PORT', 5432)
#    }
# }
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
Создайте и примените миграции БД:
```
python manage.py makemigrations
python manage.py migrate
```
Создайте суперпользователя:
```
python manage.py createsuperuser
```
Запустите локальный сервер разработки:
```
python manage.py runserver 127.0.0.1:10000
```
Открываем еще одно окно терминала, скачиваем контейнер с Redis:
```
docker pull redis
```
И запускаем его в режиме демона:
```
docker run -d --name redis -p 6379:6379 redis
```
Запускаем воркер Celery (**_в отдельном окне консоли_**, открытом по тому же пути, т.е. в папке /backend):
```
celery -A music_shop.celery worker -l info
```
**_Опционально:_** Запуск Flower (**_в отдельном окне консоли_**, открытом по тому же пути, т.е. в папке /backend). Мониторинг задач в celery будет доступен по http://127.0.0.1:5555
```
celery -A music_shop.celery flower
```

Перейдите в браузере по ссылке http://127.0.0.1:10000/admin/, вам будет доступна админка.

Flower доступен по http://127.0.0.1:5555 
с логином/паролем, заданным вами в .env (по умолчанию - _admin_ / _MySuperStrongPassword_).

</details>

<details>

<summary>Инструкция по запуску в Docker-контейнерах</summary>

### **_Запуск в контейнерах._**

Клонируйте репозиторий с **develop веткой** к себе на машину:
```
git clone git@github.com:trsv-dev/music_shop.git -b develop
```
Перейдите в папку проекта:
```
cd music_shop/
```
Переименовать **.env.example** в **.env**.

Убедитесь, что конфигурация Celery в .env настроена на использование в контейнерах.
Она должна выглядеть так:
```
#Celery settings:
###############################################################################

#### Uncomment these two strings if you use it in Docker:
#### Comment it if you use in in local development:
CELERY_BROKER_URL='redis://redis:6379/0'
CELERY_RESULT_BACKEND='redis://redis:6379/0'

#### Uncomment these two strings if you use in in local development.
#### Comment it if you use Docker:
#CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
#CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0'

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
```
Чтобы работало оповещение покупателя и админа о новом заказе, 
в .env замените раздел с email на тестовые настройки (используйте свой почтовый 
аккаунт, т.к. тестовый аккаунт может перестать работать):
```
#Email settings:
###############################################################################
RECIPIENT_ADDRESS='trsv.dev@yandex.ru'
EMAIL_HOST='smtp.yandex.ru'
EMAIL_PORT=465
EMAIL_USE_SSL=True
DEFAULT_FROM_EMAIL='trsv.dev@yandex.ru'
EMAIL_HOST_USER='trsv.dev@yandex.ru'
EMAIL_HOST_PASSWORD='hzitlzdryltagtly'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
```
и укажите email администратора (замените на свой):
```
ADMIN_EMAIL=admin@email.xoxo
```
Закомментируйте в **/backend/music_shop/settings.py** секцию, отвечающую за 
настройки SQLite и раскомментируйте секцию с PostgreSQL. Это должно выглядеть так:
```
# SQLite's settings (for local development):
###############################################################################

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# PostgreSQL's settings (for production or locally in containers):
###############################################################################

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': os.getenv('POSTGRES_DB', 'django'),
       'USER': os.getenv('POSTGRES_USER', 'django'),
       'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'you_need_to_set_the_password_in_env'),
       'HOST': os.getenv('DB_HOST', 'localhost'),
       'PORT': os.getenv('DB_PORT', 5432)
   }
}
```

Запустите контейнер в фоновом режиме:
```
docker compose -f docker-compose.yml up -d
```
Выполните и примените миграции БД (выполнять последовательно):
```
docker compose -f docker-compose.yml exec backend python manage.py makemigrations
docker compose -f docker-compose.yml exec backend python manage.py migrate
```
Соберите и скопируйте статику (выполнять последовательно):
```
docker compose -f docker-compose.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /app/static/
```
Создайте суперпользователя:
```
docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

Перейдите в браузере по ссылке http://127.0.0.1:10000/admin/, вам будет доступна админка.

Flower доступен по http://127.0.0.1:5555 
с логином/паролем, заданным вами в .env (по умолчанию - _admin_ / _MySuperStrongPassword_).

</details>
<details>
<summary>Эндпоинты</summary>

Все эндпоинты и возможные запросы описаны в [документации](https://documenter.getpostman.com/view/26097853/2sA3JGgPwv).
</details>