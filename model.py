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
    btc_count = FloatField()
    usd_count = FloatField()
    serial = IntegerField()
    class Meta:
        database = db

# Create the table
db.connect()
db.create_tables([BitcoinInfo])

def create_bitcoin_info(objin):
    bitcoin_info = BitcoinInfo(
        type = objin["type"],
        holder_count = objin["holder_count"],
        serial = objin["serial"],
        btc_count = objin["btc_count"],
        usd_count = objin["usd_count"]
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


def getLatestNDaysData(day: int):
    limit = day*4
    latest_records = (BitcoinInfo
                        .select()
                        .order_by(BitcoinInfo.created_at.desc())
                        .limit(limit))
    return latest_records

def getHolderCountAndDelta(dict1, dict2):
    # Initialize a dictionary to store the deltas
    deltas = {}

    # Iterate over the keys in the first dictionary
    for key in dict1:
        if key in dict2:
            # Calculate the delta of holderCount for each type
            holderDelta = dict1[key]['holderCount'] - dict2[key]['holderCount']
            btcDelta = dict1[key]['btc_count'] - dict2[key]['btc_count']
            usdDelta = dict1[key]['usd_count'] - dict2[key]['usd_count']
            
            deltas[key] = {
                "holder_delta": holderDelta,
                "holder_count": dict1[key]['holderCount'],
                "btc_delta": btcDelta,
                "btc_count": dict1[key]['btc_count'],
                "usd_delta": usdDelta,
                "usd_count": dict1[key]['usd_count'],
            }

    return deltas

def getDataByDaysDesc(length: int):
    length += 1
    allData = getLatestNDaysData(length)
    dataByDays = [{} for i in range(0, length)]
    deltas = {}
    targetData = {}
    for i in range(0, len(allData)):
        data = allData[i]
        dataByDays[int(i/4)][data.type] = {
            "time": data.created_at,
            "holderCount": data.holder_count,
            "date": getDate(data.created_at),
            "btc_count": data.btc_count,
            "usd_count": data.usd_count
        }
    print(dataByDays)
    for i in range(0, len(dataByDays)):
        if i > 0:
            dataToday = dataByDays[i-1]
            dataYesterday = dataByDays[i]
            today = dataByDays[i]['100 up']["date"]

            deltas = getHolderCountAndDelta(dataToday, dataYesterday)
            targetData[today] = deltas
    return targetData

def getDate(datetime):
    dateString = datetime.strftime('%Y-%m-%d')
    return dateString