import calendar
import json
import logging
from datetime import datetime

from bson import ObjectId
from flask import jsonify, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from kafka import KafkaProducer

from app.config import settings

log = logging.getLogger(__name__)


def empty_result():
    return []


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def cast_id_mongo(id_mongo):
    return str(id_mongo)


def get_uuid():
    return cast_id_mongo(ObjectId())


def get_datetime():
    date_new_format = "%d-%m-%Y %H:%M:%S"
    return datetime.now().strftime(date_new_format)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.FLASK_ALLOWED_EXTENSIONS


def password(pwd: str):
    log_rounds = settings.BCRYPT_LOG_ROUNDS
    hash_bytes = generate_password_hash(pwd, log_rounds)
    return hash_bytes.decode("utf-8")


def check_password(pwd_hash, pwd):
    return check_password_hash(pwd_hash, pwd)


def get_mime_type_application(type_extension: str):
    if type_extension == 'csv':
        return "text/csv"
    elif type_extension == 'xls' or type_extension == 'xlsx':
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def get_message_error(err):
    return make_response(jsonify({
        "msg": f"Ah ocurrido un error: {err}"
    }), 400)


def get_start_end_day_month(month, year):
    start_day = 1
    end_day = calendar.monthrange(year, month)[1]
    return start_day, end_day


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


def send_message(message, topic_name):
    producer = KafkaProducer(
        bootstrap_servers=f'{settings.KAFKA_SERVER_HOST}:{settings.KAFKA_SERVER_PORT}',
        value_serializer=serializer
    )
    producer.send(topic_name, message)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)
