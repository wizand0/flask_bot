import os
from app import app
from app.models import User, Todo, Sensors, db
#import app.admin
from threading import Thread
from aiohttp import web

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from app.handlers import router


FILENAME = "/data/todo.json" if "AMVERA" in os.environ else "todo.json"


async def main():
    bot = Bot(token='6164575119:AAEYx-IP2hSZgf2IpsHLztULW1I55jyhP2Q', parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
    #app.run(debug=False)






#flask db init
#flask db migrate -m "Initial migration."
#flask db upgrade



#if __name__ == '__main__':
#    with app.app_context():
#        db.create_all()
#        app.user_datastore.create_user(email='matt@nobien.net', password='password')
#    app.run()

# From Shell
# from app import db,app
# app.app_context().push()
# db.create_all()

# from cmd in the app's  folder:
# flask db init - This will add a migrations folder to your application. The contents of this folder need to be
# #added to version control along with your other source files.
# flask db migrate -m "Initial migration." - The migration script needs to be reviewed and edited, as Alembic is not
# #always able to detect every change you make to your models.
# flask db upgrade - Then you can apply the changes described by the migration script to your database

#git push amvera main:master

#https://cloud.amvera.ru/projects/flask-bot
#git push amvera dev:master --force
#
#curl --location --request POST 'https://api.telegram.org/bot6164575119:AAEYx-IP2hSZgf2IpsHLztULW1I55jyhP2Q/setWebhook' --header 'Content-Type: application/json' --data-raw '{ "url": "https://flask-bot-xabor.amvera.io"}'
#curl --location --request POST "https://api.telegram.org/bot6164575119:AAEYx-IP2hSZgf2IpsHLztULW1I55jyhP2Q/setWebhook?url=https://flask-bot-xabor.amvera.io" --header "Content-Type: application/json" --data-raw '{"url": "https://flask-bot-xabor.amvera.io"}'
#https://api.telegram.org/bot6164575119:AAEYx-IP2hSZgf2IpsHLztULW1I55jyhP2Q/setwebhook?url=https://flask-bot-xabor.amvera.io