# API Yatube

## Описание проекта

Yatube — REST API для публикаций, комментариев, сообществ и подписок.
Читать публикации, комментарии и список сообществ можно без токена.
Для записи и работы с подписками нужен JWT. Изменять и удалять
публикации и комментарии может только их автор.

## Установка

В корне проекта создайте виртуальное окружение.

```bash
python -m venv .venv
```

Активируйте его командой `source .venv/bin/activate` в Linux или macOS
либо `.\.venv\Scripts\Activate.ps1` в PowerShell.
Установите зависимости, примените миграции и запустите сервер.

```bash
python -m pip install -r requirements.txt
python yatube_api/manage.py migrate
python yatube_api/manage.py runserver
```

[Документация ReDoc](http://127.0.0.1:8000/redoc/)

## Примеры запросов к API

Получить список публикаций с пагинацией.

```bash
curl 'http://127.0.0.1:8000/api/v1/posts/?limit=10&offset=0'
```

Для запросов с авторизацией создайте локального пользователя командой
`python yatube_api/manage.py createsuperuser`. Подставьте его имя и пароль
в запрос на получение токена.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/jwt/create/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"myuser","password":"my-password"}'
```

Создать публикацию. Вместо `ACCESS_TOKEN` подставьте поле `access` из ответа.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H 'Authorization: Bearer ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"text":"Моя первая публикация"}'
```

Найти подписки по имени пользователя.

```bash
curl 'http://127.0.0.1:8000/api/v1/follow/?search=alice' \
  -H 'Authorization: Bearer ACCESS_TOKEN'
```
