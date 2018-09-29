import logging
import datetime
import json
import urllib
import urllib.request as request
from datetime import datetime
import json
import configparser

class DateTimeEncoder(json.JSONEncoder):
    ## Special encoder for JSONEncoder, so that DateTime objects can be serialized.
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

config = configparser.ConfigParser()
config.read('config.ini')

LOG_FORMAT = "%(name)s %(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log.Log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger(__name__)
logger.info("Logger is at level: {}".format(logger.level))


def createVehicles():
    '''Gets the JSON of 1000 vehicles, randomly generated, then outputs to a file.'''
    mockaroo_request = request.urlopen('https://my.api.mockaroo.com/vehicles.json?key={}'.format(config['DEFAULT']['MOCKAROO_API_KEY']))
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data.decode('utf-8'))
        logger.debug( "First row of data, vehicles: {}".format(json_data[0]))
        for item in json_data:
            item['nextService'] = 5000
            item['code'] = ''
        with open('vehicles.json', 'w') as f:
            f.write("[")
            for item in json_data[:len(json_data)-1]:
                f.write("%s,\n" % json.dumps(item))
            f.write("%s]" % json.dumps(json_data[len(json_data)-1]))
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))

def createCustomers():
    '''Gets the JSON of 1000 customers, randomly generated, then outputs to a file.'''
    mockaroo_request = request.urlopen('https://my.api.mockaroo.com/customers.json?key={}'.format(config['DEFAULT']['MOCKAROO_API_KEY']))
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data.decode('utf-8'))
        logger.debug( "First row of data, customers: {}".format(json_data[0]))
        print(json_data[0])
        with open('customers.json', 'w') as f:
            f.write("[")
            for item in json_data[:len(json_data)-1]:
                f.write("%s,\n" % json.dumps(item))
            f.write("%s]" % json.dumps(json_data[len(json_data)-1]))
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))

def createReservations():
    '''Gets the JSON of 1000 of reservations, randomly generated, then outputs to a file.'''
    mockaroo_request = request.urlopen('https://my.api.mockaroo.com/reservations.json?key={}'.format(config['DEFAULT']['MOCKAROO_API_KEY']))
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data.decode('utf-8'))
        for item in json_data:
            item['start_date'] = datetime.strptime(item['start_date'], '%Y-%m-%d %H:%M:%S')
            item['end_date'] = datetime.strptime(item['end_date'], '%Y-%m-%d %H:%M:%S')
        logger.debug( "First row of data, reservations: {}".format(json_data[0]))
        with open('reservations.json', 'w') as f:
            f.write("[")
            for item in json_data[:len(json_data)-1]:
                f.write("%s,\n" % json.dumps(item, cls = DateTimeEncoder))
            f.write("%s]" % json.dumps(json_data[len(json_data)-1], cls = DateTimeEncoder))
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))
