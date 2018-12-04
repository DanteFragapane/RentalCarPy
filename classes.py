class Vehicles:
    count = 0

    def __init__(self, vehicles):
        self.vehicles = vehicles
        Vehicles.count = len(self.vehicles)

    def __len__(self):
        return len(self.vehicles)

    def __iter__(self):
        return iter(self.vehicles)

    def __getitem__(self, item):
        return self.vehicles[item]


class Vehicle:
    def __init__(self, id, vin, make, model, year, color, mileage, status, nextService, code=''):
        # I decided to separate all the assignments for readability reasons.
        self.id = id
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.mileage = mileage
        self.status = status
        self.nextservice = nextService
        self.code = code
        self.ra = 0  # Rental Agreement

    def setcode(self, code):
        """Set the code on the vehicle"""
        self.code = code

    def domaintenance(self):
        """Do the maintenance"""
        self.code = ''

    def rentvehicle(self, ra):
        self.ra = ra

    def returnvehicle(self, mileage, qsp=''):
        self.ra = 0
        self.mileage += mileage
        if qsp != '':
            self.code = qsp + " " + self.code

    def __str__(self):
        """Vehicle to string"""
        return "{}:{} QSP: {}".format(self.id, self.vin, self.code)


class Reservation:
    def __init__(self, id, start_date, end_date, car_class, location=None, renterid=None):
        self.ra = id
        self.rentdate = start_date
        self.returndate = end_date
        self.carclass = car_class
        self.location = location
        self.renterid = renterid

    def __str__(self):
        return "{}: {} to {}, {}. from {}, renter: {}".format(self.ra, self.rentdate, self.returndate, self.carclass,
                                                              self.location, self.renterid)


class Customer:
    def __init__(self, id, first_name, last_name, email, address, company=None):
        self.id = id
        self.firstname = first_name
        self.lastname = last_name
        self.email = email
        self.address = address
        self.company = company
