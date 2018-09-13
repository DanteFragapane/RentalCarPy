import urllib
import urllib.request as request
import json
import logging
import datetime

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log.Log",
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger(__name__)
logger.info("Logger is at level: {}".format(logger.level))

def createVehicles():
    '''Gets the JSON of 1000 vehicles, randomly generated, then outputs to a file.'''
    mockaroo_request = request.urlopen('https://my.api.mockaroo.com/vehicles.json?key=126468d0')
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data)
        logger.debug( "First row of data, vehicles: {}".format(json_data[0]))
        with open('vehicles.json', 'w') as f:
            for item in json_data:
                item['nextService'] = 5000
                f.write("%s\n" % item)
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))

def createCustomers():
    '''Gets the JSON of 1000 customers, randomly generated, then outputs to a file.'''
    mockaroo_request = request.urlopen('https://my.api.mockaroo.com/customers.json?key=126468d0')
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data)
        logger.debug( "First row of data, customers: {}".format(json_data[0]))
        print(json_data[0])
        with open('customers.json', 'w') as f:
            for item in json_data:
                f.write("%s\n" % item)
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))

def createReservations():
    '''Gets the JSON of 1000 of reservations, randomly generated, then outputs to a file.'''
    mockaroo_request = request.urlopen('https://my.api.mockaroo.com/reservations.json?key=126468d0')
    if mockaroo_request.getcode() == 200:
        data = mockaroo_request.read()
        json_data = json.loads(data)
        for item in json_data:
            item['start_date'] = datetime.datetime.strptime(item['start_date'], '%Y-%m-%d %H:%M:%S')
        json_data.sort(key = lambda vehicle: vehicle['start_date'])
        logger.debug( "First row of data, reservations: {}".format(json_data[0]))
        with open('reservations.json', 'w') as f:
            for item in json_data:
                print(item)
                f.write("%s,\n" % item)
    else:
        logger.fatal("createVehicles: request returned {}".format(mockaroo_request.getCode()))


##createVehicles()
##createCustomers()
createReservations()
