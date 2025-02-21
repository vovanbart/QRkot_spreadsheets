# Приложение для Благотворительного фонда поддержки котиков QRkot_spreadseets

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```python
git clone https://github.com/vovanbart/QRkot_spreadsheets.git
```

Cоздать и активировать виртуальное окружение:

```python
python -m venv venv
```

```python
 . venv/Scripts/activate
```

Обновить версию ```pip``` и установить зависимости из ```requirements.txt```:

```python
python3 -m pip install --upgrade pip
```

```python
pip3 install -r requirements.txt
```

Необходимо изменить ключи, при необходимости, в файле .env.example и переименовать файл в .env (либо оставить как есть просто переименовав файл):

```python
APP_TITLE=Кошачий благотворительный фонд
APP_DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET
FIRST_SUPERUSER_EMAIL=admin@adm.ru
FIRST_SUPERUSER_PASSWORD=string
```

Применить миграции создав новую БД либо можно воспользоваться тестовой:

```python
alembic upgrade head
```

Запуск проекта:

```python
uvicorn app.main:app --reload
```

Если возникнет ошибка попробуйте изменить порт:

```python
uvicorn app.main:app --reload --port 5000
```

Документацию по API можно посмотреть по адресу:

```python
http://127.0.0.1:8000/docs
```

# Upd: + API google

Добавлены  ключи, в файле .env.example:

```python
EMAIL=example@gmail.com - Ваш email от учетной записи Гугл
```

Далее файл необходимо заполнить согласно полученного Json ключа в Google Cloud Platform создав сервисный аккаунт. <https://console.cloud.google.com/projectselector2/home/dashboard>

И подключить два API - ```Google Drive API``` и ```Google Sheets API```.

```python
TYPE=type
PROJECT_ID=project_id
PRIVATE_KEY_ID=private_key_id
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=xxx.gserviceaccount.com
CLIENT_ID=client_id
AUTH_URI=https://
TOKEN_URI=https://
AUTH_PROVIDER_X509_CERT_URL=https://
CLIENT_X509_CERT_URL=https://
```

Автор: [Владимир Б.](https://github.com/vovanbart/)
