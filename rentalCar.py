import configparser
import contextlib
import datetime
import logging
import os.path
import random
import sqlite3
from datetime import timedelta

import mysql.connector as connector

import createTablesDB as dB
import returnVehicle as rV
from classes import Customer, Reservation, Vehicle, Vehicles

config = configparser.ConfigParser()
config.read('config.ini')

LOG_FORMAT = "%(name)s %(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="log.Log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger(__name__)
logger.info("Logger is at level: {}".format(logger.level))

vehicleClasses = {"PCAR": 0, "FCAR": 0, "SCAR": 0, "ICAR": 0, "CCAR": 0, "ECAR": 0, "PFAR": 0, "FFAR": 0, "SFAR": 0,
                  "IFAR": 0, "SSAR": 0}


def get_reservations_today(reservations, goingout=False, year=0000, month=00, day=00):
    """Find all the reservations that are either going out on a date, or coming back on a date."""
    if goingout:
        outin = 'start_date'  # If a car is going out, the index we search for will have to be 'start_date'
    else:
        outin = 'end_date'
    reservationstoday = []
    if year == 0000 or month == 00 or day == 00:
        date = str(datetime.datetime.now())[:10]
    else:
        date = str(datetime.datetime(year, month, day))[:10]
    for res in reservations:
        resdate = res[outin][:10]
        if resdate == date:
            reservationstoday.append(res)
    logger.debug("Reservations for today: {}".format(reservationstoday))
    return reservationstoday


def count_class(reservations):
    """Counts the amount of vehicles in the reservations list and returns a list of amounts per class. Ex. {"PCAR": 10,
    "FCAR": 15, .... }"""
    for reserv in reservations:
        vehicleClasses[reserv['vehicle_class']] += 1
    return vehicleClasses


def date_range(startdate, enddate):
    """Gives a generator for a range of dates so they can be iterated over using a range function. Reminder: range is
    exclusive. Use the date you want to end with plus one day."""
    for n in range(int((enddate - startdate).days)):
        yield startdate + timedelta(n)


def step(vehicles):
    qsp = ''
    for vehicle in vehicles:
        if vehicle['status'] == 'rented':
            newmiles = vehicle['mileage'] + random.randint(10, 2500)
            rand = random.randint(1, 10)
            if rand == 1:
                qsp = 'GLASS'
            elif rand == 2:
                qsp = 'BD'
            rV.returnvehicle(vehicle, newmiles, qsp=qsp)
        elif vehicle['status'] == 'returned':
            rV.rentvehicle(vehicle)
        else:
            logger.warning("{}:{} IS NEITHER RENTED NOR RETURNED".format(vehicle['id'], vehicle['vin']))


def main(vehicles):
    step(vehicles)


if not os.path.isfile('rental.db'):
    dB.create_db()
    dB.create_vehicles()
    dB.create_customer()
    dB.create_reservations()

with contextlib.closing(connector.connect(host=config['DEFAULT']['HOST'], database=config['DEFAULT']['DATABASE'],
                                          user=config['DEFAULT']['USER'],
                                          password=config['DEFAULT']['PASSWORD'])) as con:
    cur = con.cursor(buffered=True)
    cur.execute('SELECT * FROM vehicles')
    vehicles = cur.fetchall()
    cur.execute('SELECT * FROM customers')
    customers = cur.fetchall()
    cur.execute('SELECT * FROM reservations')
    reservations = cur.fetchall()

    keysvehicle = (
        'id', 'vin', 'make', 'model', 'year', 'color', 'mileage', 'status', 'nextService', 'code')
    keyscustomer = ('id', 'first_name', 'last_name', 'email', 'address', 'company')
    keysreservation = ('id', 'start_date', 'end_date', 'car_class', 'location')
    for i, vehicle in enumerate(vehicles):
        vehicles[i] = dict(zip(keysvehicle, vehicle))
    for i, customer in enumerate(customers):
        customers[i] = dict(zip(keyscustomer, customer))
    for i, reserv in enumerate(reservations):
        reservations[i] = dict(zip(keysreservation, reserv))
    print(vehicles)
    print(customers)
    print(reservations)

# rv.auditvehicles(vehicles)

# main(vehicles)


# with contextlib.closing(connector.connect(host=config['DEFAULT']['HOST'], database=config['DEFAULT']['DATABASE'],
#                                           user=config['DEFAULT']['USER'],
#                                           password=config['DEFAULT']['PASSWORD'])) as con:
#     cur = con.cursor()
#     list_vehicle = []
#     cur.execute("SELECT * FROM vehicles")
#     print(cur.fetchall())
#     for veh in vehicles:
#         vehdata = (
#             veh['id'], veh['vin'], veh['make'], veh['model'], veh['year'], veh['color'], veh['mileage'], veh['status'],
#             veh['nextService'], '')
#         print(vehdata)
#         list_vehicle.append(
#             Vehicle(**veh))
#         # cur.execute("INSERT INTO vehicles VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", vehdata)
#         # con.commit()
#
#     vehicles0 = Vehicles(list_vehicle)
#
#     list_cust = []
#     for cus in customers:
#         list_cust.append(Customer(**cus))
#
#     list_reserv = []
#     for reserv in reservations:
#         list_reserv.append(Reservation(**reserv))
