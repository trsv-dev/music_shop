# Music shop

### Магазин музыкальных инструментов


## Описание

Это пэт-проект, главной целью которого является написание api и 
фронтенда магазина музыкальных инструментов.


## Работа над проектом в dev-режиме

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
python3.11 -m venv venv
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
в .env замените раздел с email на тестовые настройки:
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
в .env замените раздел с email на тестовые настройки:
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
<summary>Информация об эндпоинтах</summary>

_**Информация по эндпоинтам будет дополняться**_

### **_Общие эндпоинты:_**

Стартовый эндпоинт api: http://127.0.0.1:10000/api/v1/

Все товары: http://127.0.0.1:10000/api/v1/items/

Все категории: http://127.0.0.1:10000/api/v1/categories/

Все записи в блоге: http://127.0.0.1:10000/api/v1/blog/

Скидки: http://127.0.0.1:10000/api/v1/discount/

Специальные предложения: http://127.0.0.1:10000/api/v1/special_offer/

### **_Работа с корзиной:_**

**Просмотр корзины:**
http://127.0.0.1:10000/api/v1/cart/

Принимается GET-запрос.

**Добавление товара в корзину:**
http://127.0.0.1:10000/api/v1/add_to_cart/

Пример POST-запроса для добавления товара в корзину:
```
{
    "item_id": 1,
    "quantity": 5
}
```
где _"item_id"_ это id товара, _"quantity"_ - количество товара

**Обновление количества товара в корзине:**
http://127.0.0.1:10000/api/v1/update_cart/

Пример POST-запроса для изменения количества товара в корзине:

_Увеличение количества:_

```
{
    "item_id": 1,
    "quantity": 10
}
```
_Уменьшение количества:_
```
{
    "item_id": 1,
    "quantity": -5
}
```


**Очистка корзины:**
http://127.0.0.1:10000/api/v1/delete_cart/

Пример POST-запроса:
```
{}
```
или пустой POST-запрос.

**Оформление заказа:**
http://127.0.0.1:10000/api/v1/checkout/

Пример POST-запроса:

```
{
  "first_name": "Иван",
  "last_name": "Иванов",
  "address": "г. Балалайкин, ул. им. Ф. Меркьюри, д. 1, кв. 2",
  "email": "ready_to_rock@music.xxx",
  "communication_method": "Вот мой телефон +70000000000",
  "order_notes": "Доставить заказ вечером"
}
```
</details>