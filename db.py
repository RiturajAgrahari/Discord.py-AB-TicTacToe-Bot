import os
from tortoise import Tortoise
from dotenv import load_dotenv

load_dotenv()


async def db_init():
    # info_logger.info(f"Initializing tortoise ORM...")
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
    # info_logger.info(f"tortoise ORM is initialized successfully!")

