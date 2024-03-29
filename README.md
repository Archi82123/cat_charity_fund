# QRKot - Благотворительный фонд поддержки котиков

QRKot - это приложение для Благотворительного фонда поддержки котиков. Фонд собирает пожертвования на различные целевые проекты.

## Описание

### Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана, проект закрывается.

### Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Пожертвования поступают в проекты по принципу First In, First Out.

### Пользователи

Целевые проекты создаются администраторами сайта. Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

## API Роуты

### Charity Project

- `POST /charity_project/`: Создание нового целевого проекта.
- `GET /charity_project/`: Получение списка всех целевых проектов.
- `DELETE /charity_project/{project_id}/`: Удаление целевого проекта.
- `PATCH /charity_project/{project_id}/`: Обновление информации о целевом проекте.

### Donation

- `POST /donation/`: Создание нового пожертвования.
- `GET /donation/`: Получение списка всех пожертвований (только для администраторов).
- `GET /donation/my`: Получение списка пожертвований пользователя.

### User

- `/auth/jwt`: Роуты для аутентификации через JWT.
- `/auth`: Роуты для регистрации пользователей.
- `/users`: Роуты для работы с пользователями (получение, обновление).

## Установка и Запуск

1. Установите зависимости: `pip install -r requirements.txt`
2. Создайте и примените миграции: `alembic upgrade head`
3. Запустите приложение: `uvicorn main:app --reload`

## Конфигурация

Для настройки приложения, вы можете внести изменения в файл `.env`.
