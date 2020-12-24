from sqlalchemy import (Column, Integer, String, Sequence, Boolean)
from sqlalchemy import sql
from utils.db_api.database import db


# Создаем класс таблицы товаров
class Rest(db.Model):
    __tablename__ = 'restaurants'
    query: sql.Select

    # Уникальный идентификатор товара
    id = Column(Integer, Sequence('rest_id_seq'), primary_key=True)

    # Имя ресторана (для отображения в колбек дате)
    rest_name = Column(db.String(50))

    # Уникальный код ресторана (для отображения в колбек дате)
    rest_code = Column(String(20))

    # Логин владельца (для отображения в кнопке)
    login = Column(String(50))

    # Пароль владельца (для отображения в колбек дате)
    password = Column(String(50))

    # Номер телефона ресторана (для отображения в кнопке)
    phone = Column(String(50))

    # Описание ресторана
    description = Column(String(255))


class Course(db.Model):
    __tablename__ = 'courses'
    query: sql.Select

    # Уникальный идентификатор товара
    id = Column(Integer, Sequence('plate_id_seq'), primary_key=True)

    # Название блюда (для отображения в колбек дате)
    name = Column(db.String(50))

    # Тип меню (для отображения в кнопке)
    menu_type = Column(String(50))

    # Тип блюда (для отображения в кнопке)
    course_type = Column(String(50))

    price = Column(Integer)

    # Описание блюда
    description = Column(String(255))

    # Название ресторана (для отображения в кнопке)
    rest = Column(String(50))

    course_code = Column(String(50))


class Order(db.Model):
    __tablename__ = 'user_orders'
    query: sql.Select

    # Уникальный идентификатор юзера
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)

    # Имя юзера
    username = Column(String(50))

    # Список заказа
    order_list = Column(String(255))

    # Сумма заказа
    total_price = Column(Integer)

    def __repr__(self):
        return f"""
Цена: {self.price}"""
