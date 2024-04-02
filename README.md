# Music shop

### Магазин музыкальных инструментов


## Описание

Это пэт-проект, главной целью которого является написание api и 
фронтенда магазина музыкальных инструментов.


## Работа над проектом в dev-режиме

<details>

<summary>Инструкция по запуску</summary>

### **_Вариант 1. Запуск из консоли._**

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
Перейдите в браузере по ссылке http://127.0.0.1:10000/admin/, вам будет доступна админка.

### **_Вариант 2. Запуск Docker-контейнера._**

Клонируйте репозиторий с **develop веткой** к себе на машину:
```
git clone git@github.com:trsv-dev/music_shop.git -b develop
```
Перейдите в папку проекта:
```
cd music_shop/
```
Переименовать **.env.example** в **.env**.

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

Теперь вам должны быть доступны эндпоинты, описанные ниже.

### **_Отправка почты._**

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