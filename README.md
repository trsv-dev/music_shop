# Music shop

### Магазин музыкальных инструментов


## Описание

Это пэт-проект, главной целью которого является написание api и 
фронтенда магазина музыкальных инструментов.


## Запуск проекта в dev-режиме
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
_(Информация по эндпоинтам будет дополняться)_

Перейдите в браузере по ссылке http://127.0.0.1:10000, вам будет доступна админка по 
http://127.0.0.1:10000/admin/ и стартовый эндпоинт api http://127.0.0.1:10000/api/v1/

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

**Очистка корзины:**
http://127.0.0.1:10000/api/v1/delete_cart/

Пример POST-запроса:
```
{}
```
или пустой POST-запрос.