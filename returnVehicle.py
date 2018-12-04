import contextlib
import sqlite3


def returnvehicle(vehicle, newmiles, qsp=''):
    """Return the vehicle"""
    if vehicle['status'] == 'rented':
        with contextlib.closing(sqlite3.connect('rental.db')) as con:
            with con as cur:
                formatted = "{}:{}".format(vehicle['id'], vehicle['vin'])
                cur.execute('UPDATE vehicles SET status = "returned", mileage = ? WHERE id = ?',
                            (newmiles, vehicle['id']))  # Set the vehicle to returned
                print(formatted + " is being returned with {} miles.".format(newmiles))

                if qsp != '':
                    cur.execute('UPDATE vehicles SET code = ? WHERE id = ?',
                                (qsp, vehicle['id']))
                elif newmiles > vehicle['nextService']:  # Set the vehicle to PM if it needs service
                    cur.execute('UPDATE vehicles SET code = ? next service = ? WHERE id = ?',
                                ('PM', vehicle['nextService'] + 5000, vehicle['id']))
                    print(formatted + " is now a PM")


def rentvehicle(vehicle):
    """Rent the vehicle"""
    if vehicle['status'] == 'returned':
        with contextlib.closing(sqlite3.connect('rental.db')) as con:
            with con as cur:
                code = vehicle['code']
                formatted = "{}:{}".format(vehicle['id'], vehicle['vin'])
                if code == '':
                    print(formatted + " is being rented.")
                    cur.execute('UPDATE vehicles SET status = "rented" WHERE id = ?',
                                (vehicle['id'],))
                else:
                    if code == 'PM':
                        print(formatted + " is under maintenance.")
                    elif code == 'GLAS':
                        print(formatted + " glass is being replaced.")

                    cur.execute('UPDATE vehicles SET code = "" WHERE id = ?', (vehicle['id'],))


def codes(vehicle):
    """Perform maintenance, etc"""
    with contextlib.closing(sqlite3.connect('rental.db')) as con:
        with con as cur:
            cur.execute('UPDATE vehicles SET code = "" WHERE id = ?',
                        (vehicle['id'],))


def auditvehicles(vehicles):
    for vehicle in vehicles:
        print("{}:{}    {} {} {}, {}, mileage: {}, status: {} code: {}".format(vehicle['id'], vehicle['vin'],
                                                                               vehicle['year'], vehicle['make'],
                                                                               vehicle['model'], vehicle['color'],
                                                                               vehicle['mileage'],
                                                                               vehicle['status'], vehicle['code']))
