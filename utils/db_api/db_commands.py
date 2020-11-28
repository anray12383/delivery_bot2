from typing import List
from sqlalchemy import and_

from utils.db_api.database import db
from utils.db_api.models import Rest, Course


# Функция для создания нового ресторана в базе данных. Принимает все возможные аргументы, прописанные в Rest
async def add_rest(**kwargs):
    new_rest = await Rest(**kwargs).create()
    return new_rest


# Функция для вывода названий ресторанов
async def get_rests_names() -> List[Rest]:
    return await Rest.query.gino.all()


# Функция для вывода названий блюд и стоимости из выбранного ресторана в зависимости от выбранного типа блюд
async def get_courses_names(rest_name, course_type) -> List[Course]:
    return await Course.query.where(
        and_(Course.rest == rest_name,
             Course.course_type == course_type)).gino.all()



# # Функция для вывода стоимости товара в зависимости от выбранного ресторана
# async def get_courses_prices(rest_name, course_name) -> Course:
#     price = await db.select([db.func.sum()]).where(
#         and_(Course.rest == rest_name,
#              Course.name == course_name)).gino.scalar()
#     return price

# # Функция для получения объекта товара по его айди
# async def get_item(course_name) -> Course:
#     course = await Course.query.where(Course.course_name == course_name).gino.first()
#     return course


# # Функция для получения объекта товара по его айди
# async def get_item(item_id) -> Item:
#     item = await Item.query.where(Item.id == item_id).gino.first()
#     return item


# # Заготовка функции для вывода в зависимости от выбранного типа меню (нац. или евр.)
# async def get_items(menu_type) -> List[Course]:
#     return await Course.query.where(Course.menu_type == menu_type).gino.all()


# # Функция для подсчета товаров с выбранными категориями и подкатегориями
# async def count_items(course_code, subcategory_code=None):
#     # Прописываем условия для вывода (категория товара равняется выбранной категории)
#     conditions = [Course.course_code == course_code]
#
#     # Если передали подкатегорию, то добавляем ее в условие
#     if course_code:
#         conditions.append(Course.course_name == course_code)
#
#     # Функция подсчета товаров с указанными условиями
#     total = await db.select([db.func.count()]).where(
#         and_(*conditions)
#     ).gino.scalar()
#     return total

