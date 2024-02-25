from pydantic import BaseSettings

from app.core import constants


class Settings(BaseSettings):
    app_title: str = constants.APP_TITLE_DEFAULT
    database_url: str = constants.DATABASE_URL_DEFAULT
    secret: str = constants.SECRET_DEFAULT

    class Config:
        env_file = '.env'


settings = Settings()
