# Settings
APP_TITLE_DEFAULT = 'Фонд поддержки котиков'
DATABASE_URL_DEFAULT = 'sqlite+aiosqlite:///./fastapi.db'
SECRET_DEFAULT = 'SECRET'

# Models
MAX_NAME_LENGTH = 100
MIN_NAME_LENGTH = 1
MIN_AMOUNT = 1


class HTTPDetail:
    PROJECT_NOT_FOUND = 'Такого проекта нет!'
    CLOSED_PROJECT_DELETE = 'Нельзя удалить закрытый проект.'
    NON_EMPTY_PROJECT_DELETE = 'Нельзя удалить - уже были инвестиции!'
    CLOSED_PROJECT_EDIT = 'Нельзя модифицировать закрытые проекты.'
    LESS_THAN_INVESTED_AMOUNT = 'Нельзя установть сумму меньше уже внесённой.'
    DUPLICATE_PROJECT_NAME = 'Проект с таким именем уже существует!'
    INVALID_PROJECT_NAME_LENGTH = 'Имя должно быть от 1 до 100 символов.'
    INVALID_PROJECT_AMOUNT = 'Сумма проекта должна быть больше нуля.'


class UserException:
    INVALID_PASSWORD_LENGTH = 'Password should be at least 3 characters'
    INVALID_PASSWORD_CONTAIN = 'Password should not contain e-mail'
    EMAIL_ALREADY_EXISTS = 'Пользователь с таким email зарегистрирован.'
