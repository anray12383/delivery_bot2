from gino import Gino
from config import POSTGRES_URI

db = Gino()


# Документация
# http://gino.fantix.pro/en/latest/tutorials/tutorial.html

async def connect_db():
    # Устанавливаем связь с базой данных
    await db.set_bind(POSTGRES_URI)

