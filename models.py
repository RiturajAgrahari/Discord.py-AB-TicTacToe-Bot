from tortoise.models import Model
from tortoise import fields


class Profile(Model):
    id = fields.IntField(primary_key=True)
    discord_id = fields.CharField(max_length=200)
    discord_name = fields.CharField(max_length=224)
    bot_used = fields.IntField(default=0)
    # created_on = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.discord_name


class BotUsage(Model):
    id = fields.IntField(primary_key=True)
    usage = fields.IntField()
    date = fields.DatetimeField(auto_now_add=True)


class TicTacToeGame(Model):
    id = fields.IntField(primary_key=True)
    uid = fields.ForeignKeyField("models.Profile", related_name="tictactoe")
    win = fields.IntField(default=0)
    loss = fields.IntField(default=0)
    tie = fields.IntField(default=0)







