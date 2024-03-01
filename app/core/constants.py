# Settings
APP_TITLE_DEFAULT = 'Фонд поддержки котиков'
DATABASE_URL_DEFAULT = 'sqlite+aiosqlite:///./fastapi.db'
SECRET_DEFAULT = 'SECRET'
LIFETIME_SECONDS = 3600

# Models
MAX_NAME_LENGTH = 100
MIN_NAME_LENGTH = 1
MIN_AMOUNT = 1

# Users
MIN_PASSWORD_LENGTH = 3


class HTTPDetail:
    PROJECT_NOT_FOUND = 'Такого проекта нет!'
    CLOSED_PROJECT_DELETE = 'Нельзя удалить закрытый проект.'
    NON_EMPTY_PROJECT_DELETE = 'Нельзя удалить - уже были инвестиции!'
    CLOSED_PROJECT_EDIT = 'Нельзя модифицировать закрытые проекты.'
    LESS_THAN_INVESTED_AMOUNT = 'Нельзя установть сумму меньше уже внесённой.'
    DUPLICATE_PROJECT_NAME = 'Проект с таким именем уже существует!'
    INVALID_PROJECT_NAME_LENGTH = (f'Имя должно быть от {MIN_NAME_LENGTH}'
                                   f'до {MAX_NAME_LENGTH} символов.')
    INVALID_PROJECT_AMOUNT = 'Сумма проекта должна быть больше нуля.'


class UserException:
    INVALID_PASSWORD_LENGTH = ('Password should be at least'
                               f'{MIN_PASSWORD_LENGTH} characters')
    INVALID_PASSWORD_CONTAIN = 'Password should not contain e-mail'
    EMAIL_ALREADY_EXISTS = 'Пользователь с таким email зарегистрирован.'
