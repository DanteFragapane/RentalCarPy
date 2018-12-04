import configparser
import contextlib
import datetime
import json
import logging
import sqlite3
import urllib.request as request
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    # Special encoder for JSONEncoder, so that DateTime objects can be serialized.
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


config = configparser.ConfigParser()
config.read('config.ini')

LOG_FORMAT = "%(name)s %(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="log.Log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger(__name__)
logger.info("Logger is at level: {}".format(logger.level))


def create_db():
    with contextlib.closing(sqlite3.connect('rental.db')) as con:  # Contextlib.closing will automatically close the con
        with con as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS vehicles ('
                        'id int unique, vin text, make text, model text, year int, color text, mileage int, '
                        'status text, nextService int, code text'
                        ')')
            cur.execute('CREATE TABLE IF NOT EXISTS customers ('
                        'id int unique, first_name text, last_name text, email text, address text, company text '
                        ')')
            cur.execute('CREATE TABLE IF NOT EXISTS reservations ('
                        'id int unique, start_date datetime, end_date datetime, vehicle_class text, location text'
                        ')')


def create_vehicles():
    """Gets the JSON of 1000 vehicles, randomly generated, then outputs to a file."""
    mockaroo_request = request.urlopen(
        'https://my.api.mockaroo.com/vehicles.json?key={}'.format(config['DEFAULT']['MOCKAROO_API_KEY']))
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data.decode('utf-8'))
        logger.debug("First row of data, vehicles: {}".format(json_data[0]))
        for item in json_data:
            item['nextService'] = 5000
            item['code'] = ''
        with contextlib.closing(sqlite3.connect('rental.db')) as con:
            with con as cur:
                for item in json_data:
                    cur.execute('INSERT INTO vehicles VALUES (?,?,?,?,?,?,?,?,?,?)', (
                        item['id'], item['vin'], item['make'], item['model'], item['year'],
                        item['color'], item['mileage'], item['status'], item['nextService'],
                        item['code'],))
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))


def create_customer():
    """Gets the JSON of 1000 customers, randomly generated, then outputs to a file."""
    mockaroo_request = request.urlopen(
        'https://my.api.mockaroo.com/customers.json?key={}'.format(config['DEFAULT']['MOCKAROO_API_KEY']))
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data.decode('utf-8'))
        logger.debug("First row of data, customers: {}".format(json_data[0]))
        print(json_data[0])
        with contextlib.closing(sqlite3.connect('rental.db')) as con:
            with con as cur:
                for customer in json_data:
                    cur.execute('INSERT INTO customers VALUES (?,?,?,?,?,?)', (
                        customer['id'], customer['first_name'], customer['last_name'], customer['email'],
                        customer['address'], customer['company']))
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))


def create_reservations():
    """Gets the JSON of 1000 of reservations, randomly generated, then outputs to a file."""
    mockaroo_request = request.urlopen(
        'https://my.api.mockaroo.com/reservations.json?key={}'.format(config['DEFAULT']['MOCKAROO_API_KEY']))
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data.decode('utf-8'))
        for item in json_data:
            item['start_date'] = datetime.strptime(item['start_date'], '%Y-%m-%d %H:%M:%S')
            item['end_date'] = datetime.strptime(item['end_date'], '%Y-%m-%d %H:%M:%S')
        logger.debug("First row of data, reservations: {}".format(json_data[0]))
        with contextlib.closing(sqlite3.connect('rental.db')) as con:
            with con as cur:
                for reserv in json_data:
                    cur.execute('INSERT INTO reservations VALUES (?,?,?,?,?)', (
                        reserv['id'], reserv['start_date'], reserv['end_date'], reserv['vehicle_class'],
                        reserv['location']))
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))
