from home.models import Bus, Ticket, Customer, Operator, Seats
from datetime import datetime


class Result():

    def __init__(self, bus, seat):
        self.busNo = bus.busNumber
        self.busId = bus.busId
        self.busName = bus.busName
        self.goesFrom = bus.goesfrom
        self.goesTo = bus.goesTo
        self.departureTime = bus.departureTime.strftime("%X %p")
        self.arrivalTime = bus.arrivalTime.strftime("%X %p")
        self.totalSeats = bus.seats
        self.availableSeatsCount = self.totalSeats - len(seat)
        self.bookedSeats = seat
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
        self.customerId = customer.customer_id
        self.operatorId = str(operator.operator_id)
        self.customerName = customer.name
        self.customerContact = ticket.passangerContact
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

        self.departureTimeStamp = datetime.strptime(
            str(self.date) + " " + str(self.departure), '%Y-%m-%d %H:%M:%S')

        self.today = datetime.strptime(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if self.departureTimeStamp > self.today:
            self.isCompleted = False
        else:
            self.isCompleted = True


class UserAcount():
    def __init__(self, customer, tickets):

        self.name = customer.name
        self.email = customer.email
        self.wallet = customer.wallet
        self.tickets = tickets
        self.totalSpend = 0
        self.cancelled = 0
        self.completed = 0
        self.booked = 0

        self.upcommingBookings = []
        # print("ticket recence", tickets)
        if len(self.tickets) == 0:
            self.hasNoUpcomming = False
            self.upcomming = 0
        else:
            for ticket in tickets:
                if ticket.isCompleted:
                    self.completed = self.completed + 1

                elif ticket.isTicketCancelled:
                    self.cancelled = self.cancelled + 1

                else:
                    self.booked = self.booked + 1
                    self.upcommingBookings.append(ticket)

        for ticket in tickets:
            if ticket.isTicketCancelled == False:
                self.totalSpend = self.totalSpend + ticket.totalFare


class OperatorAccount():
    def __init__(self, operator, tickets):
        self.operator = operator
        self.name = operator.name
        self.email = operator.email
        self.wallet = self.operator.amountInWallet
        self.tickets = tickets
        self.totalSpend = 0
        self.cancelled = 0
        self.completed = 0
        self.booked = 0

        self.upcommingBookings = []
        # print("ticket recence", tickets)
        if len(self.tickets) == 0:
            self.hasNoUpcomming = False
            self.upcomming = 0
        else:
            for ticket in tickets:
                if ticket.isCompleted:
                    self.completed = self.completed + 1

                elif ticket.isTicketCancelled:
                    self.cancelled = self.cancelled + 1

                else:
                    self.booked = self.booked + 1
                    self.upcommingBookings.append(ticket)

        for ticket in tickets:
            if ticket.isTicketCancelled == False:
                self.totalSpend = self.totalSpend + ticket.totalFare


class BusOperatorResult():

    def __init__(self, bus):
        self.busNo = bus.busNumber
        self.busId = bus.busId
        self.busName = bus.busName

        self.goesFrom = bus.goesfrom
        self.goesTo = bus.goesTo
        self.departureTime = bus.departureTime.strftime("%X %p")
        self.arrivalTime = bus.arrivalTime.strftime("%X %p")
        self.totalSeats = bus.seats
        self.availableSeatsCount = self.totalSeats

        self.rachesOnDay = bus.arrivesOnDay
        self.isAc = bus.hasAc
        self.isSleeper = bus.isSleeper
        self.fare = bus.fare
        self.runsOn = bus.runsOn
        self.stops = bus.stops
        self.isRunning = bus.isRunning
        self.operatorAgencyName = bus.agencyName

        if "A" in self.departureTime:
            print("this. is am")
            self.isDayDeparture = True
        else:
            self.isDayDeparture = False

        if "A" in self.arrivalTime:
            self.isDayArrival = True
        else:
            self.isDayArrival = False


class checkRunning():

    def __init__(self, ticket, bus):

        self.ticketId = str(ticket.ticketId)
        self.busId = str(bus.busId)
        self.ticketFrom = bus.goesfrom
        self.ticketTo = bus.goesTo
        self.departure = bus.departureTime
        self.arrival = bus.arrivalTime
        self.date = ticket.dateOfJourney
        self.isTicketCancelled = ticket.isCancelled
        self.isBusRunning = ticket.isBusRunning
        self.bookingDate = ticket.bookingDate
        self.isSleeper = bus.isSleeper
        self.hasAc = bus.hasAc

        self.departureTimeStamp = datetime.strptime(
            str(self.date) + " " + str(self.departure), '%Y-%m-%d %H:%M:%S')

        self.today = datetime.strptime(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if self.departureTimeStamp > self.today:
            self.isCompleted = False
        else:
            self.isCompleted = True


class OperatorDashboardInfo():

    def __init__(self, operator, buses, tickets):
        self.activeRuns = []
        for bus in buses:
            if bus.isRunning == True:
                self.activeRuns.append(bus)

        if len(self.activeRuns) == 0:
            self.activeBusses = 0
        else:
            self.activeBusses = len(self.activeRuns)

        self.today = datetime.now().date()

        # importatnt variables
        self.bookedToday = 0
        self.runsToday = 0
        self.walletFilled = 0

        # print("type is", type(self.today))
        for ticket in tickets:
            print("type get ", type(ticket.bookingDate))
            self.journeyDate = datetime.strptime(
                str(ticket.dateOfJourney), '%Y-%m-%d')
            if self.today == ticket.bookingDate.date() and ticket.isCancelled == False:
                self.bookedToday += 1
                self.walletFilled += ticket.totalFare
            if self.today == self.journeyDate:
                self.runsToday += 1


class Payments():
    def __init__(self, ticketAmmount, customer):
        self.customerWallet = customer.wallet
        self.customerHearts = customer.hearts

        self.conversionRate = 0.02
        self.ammountInRupee = ticketAmmount
        self.ammountInHearts = self.ammountInRupee * self.conversionRate
