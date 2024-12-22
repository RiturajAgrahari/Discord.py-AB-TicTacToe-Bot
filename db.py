import os
from tortoise import Tortoise
from dotenv import load_dotenv
from logger import debug_logger

load_dotenv()


async def db_init():
    debug_logger.debug(f"Initializing ORM...")
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "database": os.getenv("DATABASE"),
                        "host": os.getenv("HOST"),
                        "password": os.getenv("PASSWORD"),
                        "port": os.getenv("PORT"),
                        "user": os.getenv("DB_USER"),
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["models"],
                    "default_connection": "default",
                }
            },
        }
    )

    await Tortoise.generate_schemas(safe=True)
    debug_logger.debug(f"ORM initialization successful!")

