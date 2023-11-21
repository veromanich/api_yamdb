# api_yamdb
### Описание:
Проект «API для YaMDb». YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
##
### Стек технологий:
<details>
<summary>Подробнее/свернуть</summary>

- Python 3.9.10
- Django 3.2
- DRF
- JWT
</details>

##
### Установка:
<details>
<summary>Подробнее/свернуть</summary>
  
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/veromanich/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
</details>

##
### Примеры запросов к API:
<details>
<summary>Подробнее/свернуть</summary>

### AUTH. Регистрация пользователей и выдача токенов:
```
/api/v1/auth/signup/
```
- POST - Получить код подтверждения на переданный email. Права доступа: Доступно без токена.
```json
{
"email": "user@example.com",
"username": "string"
}
```
##
```
/api/v1/auth/token/
```
- POST - Получение JWT-токена в обмен на username и confirmation code. Права доступа: Доступно без токена.
```json
{
"username": "string",
"confirmation_code": "string"
}
```
##
### CATEGORIES. Категории (типы) произведений:
```
/api/v1/categories/
```
- GET - Получить список всех категорий Права доступа: Доступно без токена.
- POST - Создать категорию. Права доступа: Администратор.
```json
{
"name": "string",
"slug": "string"
}
```
##
```
/api/v1/categories/{slug}/
```
- DELETE - Удалить категорию. Права доступа: Администратор.
##
### GENRES. Категории жанров:
```
/api/v1/genres/
```
- GET - Получить список всех жанров. Права доступа: Доступно без токена.
- POST - Добавить жанр. Права доступа: Администратор.
```json
{
"name": "string",
"slug": "string"
}
```
##
```
/api/v1/genres/{slug}/
```
- DELETE - Удалить жанр. Права доступа: Администратор.
##
### TITLES. Произведения, к которым пишут отзывы (определённый фильм, книга или песенка):
```
/api/v1/titles/
```
- GET - Получить список всех объектов. Права доступа: Доступно без токена.
- POST - Добавить новое произведение. Права доступа: Администратор.
```json
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
  "string"
],
"category": "string"
}
```
##
```
/api/v1/titles/{titles_id}/
```
- GET - Информация о произведении Права доступа: Доступно без токена.
- PATCH - Обновить информацию о произведении Права доступа: Администратор.
```json
{
"name": "string",
"year": 0,
"description": "string",
"genre": [
  "string"
],
"category": "string"
}
```
- DELETE - Удалить произведение. Права доступа: Администратор.
##
### REVIEWS. Отзывы:
```
/api/v1/titles/{title_id}/reviews/
```
- GET - Получить список всех отзывов. Права доступа: Доступно без токена.
- POST - Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение. Права доступа: Аутентифицированные пользователи.
```json
{
"text": "string",
"score": 1
}
```
##
```
/api/v1/titles/{title_id}/reviews/{review_id}/
```
- GET - Получить отзыв по id для указанного произведения. Права доступа: Доступно без токена.
- PATCH - Частично обновить отзыв по id. Права доступа: Автор отзыва, модератор или администратор.
```json
{
"text": "string",
"score": 1
}
```
- DELETE - Удалить отзыв по id Права доступа: Автор отзыва, модератор или администратор.
##
### COMMENTS. Комментарии к отзывам:
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
- GET - Получить список всех комментариев к отзыву по id Права доступа: Доступно без токена.
- POST - Добавить новый комментарий для отзыва. Права доступа: Аутентифицированные пользователи.
```json
{
"text": "string"
}
```
##
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
- GET - Получить комментарий для отзыва по id. Права доступа: Доступно без токена.
- PATCH - Частично обновить комментарий к отзыву по id. Права доступа: Автор комментария, модератор или администратор.
```json
{
"text": "string"
}
```
- DELETE - Удалить комментарий к отзыву по id. Права доступа: Автор комментария, модератор или администратор.
##
### USERS. Пользователи:
```
/api/v1/users/
```
- GET - Получить список всех пользователей. Права доступа: Администратор.
- POST - Добавить нового пользователя. Права доступа: Администратор.
```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
##
```
/api/v1/users/{username}/
```
- GET - Получить пользователя по username. Права доступа: Администратор.
- PATCH - Изменить данные пользователя по username. Права доступа: Администратор.
```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
- DELETE - Удалить пользователя по username. Права доступа: Администратор.
##
```
/api/v1/users/me/
```
- GET - Получить данные своей учетной записи Права доступа: Любой авторизованный пользователь.
- PATCH - Изменить данные своей учетной записи Права доступа: Любой авторизованный пользователь.
```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string"
}
```
</details>

##
### Авторы:
- [Артур Шакиров](https://github.com/ArtiOru)
- [Павел Борисов](https://github.com/PavelBorisovQ)
- [Роман Веренич](https://github.com/veromanich)
