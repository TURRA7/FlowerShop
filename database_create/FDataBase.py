"""Модуль создаёт таблицы и даёт инструменты для работы с ними."""
from datetime import datetime
from log_mod import Logger

from flask import flash, redirect, request, url_for

from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import DeclarativeBase


# Создание логгера
db_logger = Logger("log_FDataBase.log")
logger = db_logger.get_logger()


# Объявление базового(декларативного) класса
class Base(DeclarativeBase):
    """
    Базовый декларативный класс.

    Необходим для работы с метаданными таблиц.
    """

    pass


# Создание экземпляра SQLAlchemy
db = SQLAlchemy(model_class=Base)


class UserAdmin(UserMixin, db.Model):
    """
    Класс создаёт таблицу с адмнистраторами проекта.

    :param id: Является id индификатором пользователя.
    :param username: логин пользователя.
    :param password: Пороль пользователя.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(300), nullable=False)
    password: str = db.Column(db.String(300), nullable=False)


class Item(UserMixin, db.Model):
    """Класс создаёт таблицу с товарами для каталога."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(255))

    def __init__(self, name: str, description: str,
                 price: int, category: int, photo: str):
        """
        Параметры для работы метода.

        :param id: Является id индификатором товара.
        :param name: название товара.
        :param description: Описание товара.
        :param price: Цена товара.
        :param category: Категория товара.
        :param photo: Название файла с расширением.
        """
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.photo = photo


class Article(UserMixin, db.Model):
    """Класс создаёт таблицу с новостями."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255))
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name: str, text: str,
                 photo: str, pub_date: datetime):
        """
        Параметры для работы метода.

        :param id: Является id индификатором новости.
        :param name: Заголовок новости.
        :param text: текст новости.
        :param photo: Название файла с расширением.
        :param pub_date: Дата и время загрузки новости.
        """
        self.name = name
        self.text = text
        self.photo = photo
        self.pub_date = pub_date


class DeleteItems:
    """Класс для удаления айтемов из базы данных."""

    def __init__(self, name_id: str, table_db: object,
                 name_page: str, delete_form: object):
        """
        Параметры для работы метода.

        :param name_id: Название категории айтема.
        :param table_db: Название таблицы, из которой будет удалён айтем.
        :param name_page: Название страницы с которой будет удалён айтем.
        :param delete_form: Объект класса DeleteItemsForm
        """
        self.name_id = name_id
        self.table_db = table_db
        self.name_page = name_page
        self.delete_form = delete_form

    def delete_items(self):
        """Метод удалаяет айтем из базы данных."""
        if request.method == 'POST':
            if self.delete_form.validate_on_submit():
                item_id = request.form.get(self.name_id)
                item = self.table_db.query.get(item_id)
                if item:
                    try:
                        logger.debug("Айтем удалён!: %s", self.name_id)
                        db.session.delete(item)
                        db.session.commit()
                        return redirect(url_for(self.name_page))
                    except Exception as ex:
                        # Запись информации об ошибках в логи.
                        logger.debug("Ошибка при удалении товара: %s %s",
                                     ex, self.name_id)
            else:
                # !!! ПОСЛЕ ПРОВЕДЕНИЯ ТЕСТОВ, ДАННУЮ СТРОКУ УБРАТЬ !!!
                flash('Ошибка при удалении товара', 'error')
