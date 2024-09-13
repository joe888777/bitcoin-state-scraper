from peewee import *
from datetime import datetime, timezone
from playhouse.postgres_ext import DateTimeTZField
from config import settings


db = PostgresqlDatabase(
    settings.POSTGRES_DB_NAME,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
)

class BaseModel(Model):
    id = AutoField(primary_key=True)
    created_at = DateTimeTZField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeTZField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        if self.updated_at:
            self.updated_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)

class BitcoinInfo(BaseModel):
    type = CharField(null=False)
    holder_count = IntegerField()
    serial = IntegerField()
    class Meta:
        database = db

# Create the table
db.connect()
db.create_tables([BitcoinInfo])

def create_bitcoin_info(type, holder_count, serial):
    bitcoin_info = BitcoinInfo(
        type = type,
        holder_count = holder_count,
        serial = serial
    )
    bitcoin_info.save()
    return bitcoin_info

def get_bitcoin_info(id):
    bitcoin_info = BitcoinInfo.get(BitcoinInfo.id == id)
    return bitcoin_info

def update_bitcoin_info(id, data):
    bitcoin_info = BitcoinInfo.get(BitcoinInfo.id == id)
    for key, value in data.items():
        setattr(bitcoin_info, key, value)
    bitcoin_info.save()
    return bitcoin_info

def get_bitcoin_infos():
    bitcoin_infos = BitcoinInfo.select()
    return bitcoin_infos

def delete_bitcoin_info(id):
    bitcoin_info = BitcoinInfo.get(BitcoinInfo.id == id)
    bitcoin_info.delete_instance()
    return bitcoin_info

def get_latest_bitcoin_serial():
    try:
        bitcoin_info = BitcoinInfo.select().order_by(BitcoinInfo.id.desc()).limit(1)
        print("ggg")
    except:
        return None;

    return bitcoin_info;