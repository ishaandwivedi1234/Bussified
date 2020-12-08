from home.models import Bus


class Result():

    def __init__(self, bus):
        self.busNo = bus.busNumber
        self.busId = bus.busId
        self.busName = bus.busName
        self.goesFrom = bus.goesfrom
        self.goesTo = bus.goesTo
        self.departureTime = bus.departureTime.strftime("%X %p")
        self.arrivalTime = bus.arrivalTime.strftime("%X %p")
        self.totalSeats = bus.seats
        self.availableSeatsCount = self.totalSeats - len(bus.bookedSeats)
        self.bookedSeats = bus.bookedSeats
        self.rachesOnDay = bus.arrivesOnDay
        self.isAc = bus.hasAc
        self.isSleeper = bus.isSleeper
        self.fare = bus.fare
        self.runsOn = bus.runsOn
        self.stops = bus.stops
        self.isRunning = bus.isRunning
        self.operatorAgencyName = bus.agencyName

        if self.availableSeatsCount < 0:
            self.availableSeatsCount = 0

        if "A" in self.departureTime:
            print("this. is am")
            self.isDayDeparture = True
        else:
            self.isDayDeparture = False

        if "A" in self.arrivalTime:
            self.isDayArrival = True
        else:
            self.isDayArrival = False
