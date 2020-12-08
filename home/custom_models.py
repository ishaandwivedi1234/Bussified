from home.models import Bus, Ticket, Customer, Operator


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


class Bookings():

    def __init__(self, ticket, customer, bus, operator):

        self.ticketId = str(ticket.ticketId)
        self.busId = str(bus.busId)
        self.operatorId = str(operator.operator_id)

        self.ticketFrom = bus.goesfrom
        self.ticketTo = bus.goesTo
        self.departure = bus.departureTime
        self.arrival = bus.arrivalTime
        self.agencyName = bus.agencyName
        self.passengerName = ticket.passangerName
        self.bookedSeats = ticket.bookedSeats
        self.totalFare = ticket.totalFare
        self.date = ticket.dateOfJourney
        self.isTicketCancelled = ticket.isCancelled
        self.isBusRunning = ticket.isBusRunning
        self.bookingDate = ticket.bookingDate
        self.operatorHelpline = operator.helpline
        self.operatorEmail = operator.email
        self.isSleeper = bus.isSleeper
        self.hasAc = bus.hasAc
