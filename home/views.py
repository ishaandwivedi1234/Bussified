from django.shortcuts import render, redirect
from home.models import Customer, Bus, Operator, Ticket, Seats
from django.contrib import messages
from datetime import datetime
from home.custom_models import Result, Bookings, UserAcount
from django.shortcuts import render
from yatram.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# Create your views here.


def index(request):
    password = request.POST.get("password")
    email = request.POST.get("email")

    if password and email:
        try:

            customer = Customer.objects.get(email=email, password=password)
            request.session['isLogged'] = True
            request.session['customer_id'] = customer.customer_id
            return redirect('/dashboard')

        except Exception as e:
            print(e)
            messages.warning(request, "Wrong email or password ! ")
            request.session['isLogged'] = False

    return render(request, 'index.html')


def register(request):

    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")

    if name and email and password:
        # logic to add to databse after checking if it exists or not

        try:
            customer = Customer(name=name, email=email, password=password)

            customer.save()
            message = "Hi " + name + " You have just created an account on Bussified reservations ! " +\
                "Hope you will like this project\ncontact me at ishaan.dwivedi@gmail.com "
            subject = "No-reply@customer support - Bussified"
            recepient = email.strip()
            send_mail(subject, message, EMAIL_HOST_USER,
                      [recepient, "ishaan.dwivedi99@gmail.com"], fail_silently=False)

            messages.success(
                request, "You have successfully registered with Bussified ! ")
            print("saved to database")

        except Exception as e:
            print(e)
            messages.warning(request, "You already have an account ! ")
        return render(request, 'index.html')
    return render(request, 'register.html')


def customerLogout(request):
    request.session['isLogged'] = False
    return redirect('/')


def operatorRegister(request):

    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    agency = request.POST.get("agency")
    helpline = request.POST.get("contact")
    if name and email and password and agency and helpline:
        print("Posting comming")
        # logic to add to databse after checking if it exists or not
        operator = Operator(name=name, email=email,
                            password=password, agencyName=agency, helpline=helpline)
        try:
            operator.save()
            message = "Hi " + name + " You have just created an account on Bussified reservations for bus operator ! " +\
                "Hope you will like this project\ncontact me at ishaan.dwivedi@gmail.com "
            subject = "No-reply@customer support - Bussified"
            recepient = email.strip()
            send_mail(subject, message, EMAIL_HOST_USER,
                      [recepient, "ishaan.dwivedi99@gmail.com"], fail_silently=False)

            messages.success(
                request, "You have successfully registered with Bussified ! ")
            print("saved to database")

        except:
            messages.warning(request, "You already have an account ! ")

        return redirect('/operator')

    return render(request, 'operator_register.html')


def operatorLogin(request):
    password = request.POST.get("password")
    email = request.POST.get("email")

    if password and email:
        try:
            operator = Operator.objects.get(email=email, password=password)
            print(operator.agencyName)
            request.session['isLoggedAsOperator'] = True
            request.session['operator_id'] = operator.operator_id
            return redirect('/operator/dashboard')

        except:
            messages.warning(request, 'Wrong email or password ! ')

    else:
        request.session['isLoggedAsOperator'] = False

    return render(request, 'operator_login.html')


def operatorLogout(request):
    request.session['isLoggedAsOperator'] = False
    return redirect('/operator')


def operatorDashboard(request):
    isLogged = request.session.get('isLoggedAsOperator')
    operator_id = request.session.get('operator_id')

    if operator_id == None:
        return redirect("/operator")

    context = {}
    operator = Operator.objects.get(operator_id=operator_id)
    try:
        busList = Bus.objects.filter(operator_id=str(operator.operator_id))
        print(busList)
        total_bus = len(busList)
        print(busList.first())
    except Exception as e:
        print("the exception is", e)
        total_bus = 0

    name = operator.name
    email = operator.email
    agencyName = operator.agencyName
    firstName = name.split()[0]
    context['name'] = name
    context['email'] = email
    context['operator_id'] = operator_id
    context['operator'] = operator
    context['total_bus'] = total_bus
    context['agencyName'] = agencyName.capitalize()
    context['firstName'] = firstName
    return render(request, 'operator_dashboard.html', context)


def addBus(request, operatorId):
    context = {}
    operator = Operator.objects.get(operator_id=operatorId)

    busNumber = request.POST.get('busNumber').upper()

    busName = request.POST.get('model').lower()
    acSettings = request.POST.get('acSettings').lower()
    sleeperSettings = request.POST.get('sleeperSettings').lower()
    startsFrom = request.POST.get('from').lower()
    lastStop = request.POST.get('to').lower()
    seats = request.POST.get('seats')
    fare = request.POST.get('fare')
    fareCuts = request.POST.get('fareCuts')
    runnigDays = request.POST.getlist('days')
    departureTime = request.POST.get('departure')
    arrivalTime = request.POST.get('arrival')
    arrivesOnDay = request.POST.get('arrivesOn')
    stop1 = request.POST.get('stop1').lower()
    stop2 = request.POST.get('stop2').lower()
    stop3 = request.POST.get('stop3').lower()
    stop4 = request.POST.get('stop4').lower()
    stop5 = request.POST.get('stop5').lower()
    hasAc = bool(int(acSettings))
    hasSleeper = bool(int(sleeperSettings))
    stops = [stop1.lower(), stop2.lower(), stop3.lower(),
             stop4.lower(), stop5.lower()]

    print(acSettings, "sleeper : ", sleeperSettings)
    bus = Bus(
        operator_id=operator.operator_id,
        busNumber=busNumber,
        busName=busName,
        goesfrom=startsFrom,
        goesTo=lastStop,
        seats=seats,
        fare=fare,
        stopsFareCutting=fareCuts,
        hasAc=hasAc,
        isSleeper=hasSleeper,
        runsOn=runnigDays,
        bookedSeats=[],
        stops=stops,
        arrivalTime=arrivalTime,
        departureTime=departureTime,
        arrivesOnDay=arrivesOnDay,
        agencyName=operator.agencyName
    )

    try:
        bus.save()
        messages.success(request, "Added The Bus Successfully !")
        return redirect('/operator/dashboard')
    except:
        messages.warning(request, "Something failed !")
        return redirect('/operator/dashboard')


def userDashboard(request):

    isLogged = request.session.get('isLogged')
    customer_id = request.session.get('customer_id')

    if customer_id == None:
        return redirect("/register")

    context = {}
    customer = Customer.objects.get(customer_id=customer_id)

    name = customer.name
    email = customer.email
    context['name'] = name
    context['email'] = email
    context['customerId'] = customer_id
    context['hasSearched'] = False
    context['hasSearchResultForDay'] = False
    context['hasResultsForOtherDays'] = False
    context['resultsForDay'] = []
    context['resultsForOtherDays'] = []

    resultsForDay = []
    resultsForNonDays = []

    # result of search

    fromLocation = request.POST.get('from')
    toLocation = request.POST.get('to')
    dateOfJourney = request.POST.get('date')
    if request.method == 'POST':
        if not fromLocation or not toLocation or not dateOfJourney:
            messages.warning(request, "Please fill all the fields ! ")
    if fromLocation and toLocation and dateOfJourney:
        context['hasSearched'] = True
        date = datetime.strptime(dateOfJourney, "%Y-%m-%d")
        dayOfJourney = date.strftime("%A").lower()
        fromLocation = fromLocation.lower()
        toLocation = toLocation.lower()
        print(dayOfJourney)
        try:
            bus = Bus.objects.filter(goesfrom=fromLocation, goesTo=toLocation)
            if len(bus) == 0:
                messages.warning(request, "No bus found on this route ! ")
            else:
                seatMatrix = []
                for b in bus:
                    if dayOfJourney in b.runsOn:
                        print(b.bookedSeats)

                        try:
                            seat = Seats.objects.get(busId=b.busId, date=date)
                            seatMatrix = seat.seatsBooked
                        except Exception as e:
                            print(e)

                        print("match")
                        resultsForDay.append(Result(b, seatMatrix))
                    else:
                        resultsForNonDays.append(Result(b, seatMatrix))

                context['hasResultsForOtherDays'] = True
                context['resultsForOtherDays'] = resultsForNonDays

                context['searchedDate'] = dateOfJourney
                context['searchedDay'] = dayOfJourney

                print(resultsForDay)
                print(resultsForNonDays)
                if len(resultsForDay) == 0:
                    messages.warning(
                        request, "No Busses runs on the given day of the week ! Check results for other days")

                else:
                    context['hasSearchResultForDay'] = True
                    context['resultsForDay'] = resultsForDay

        except Exception as e:
            print(e)

    return render(request, 'customer_dashboard.html', context)


def bookTickets(request, customerId, busId, date):

    context = {}
    try:
        customer = Customer.objects.get(customer_id=customerId)
        bus = Bus.objects.get(busId=busId)
        operator = Operator.objects.get(operator_id=bus.operator_id)
        seatMatrix = []
        gotSeat = False
        try:
            seats = Seats.objects.get(busId=busId, date=date)
            seatMatrix = seats.seatsBooked
            gotSeat = True
        except Exception as e:
            print(e)
            gotSeat = False

        context['name'] = customer.name
        context['bus'] = Result(bus, seatMatrix)
        context['customer'] = customer
        context['dateOfJourney'] = date

        # booking logic
        seatsSelected = request.POST.getlist('seatsSelected')

        print(seatMatrix)

        mobile = request.POST.get('mobile')

        if mobile:
            if len(seatsSelected) == 0:
                messages.warning(
                    request, "Please select atleast 1 seat to book a ticket !")
            else:
                totalBookedSeats = []

                ticket = Ticket(
                    passengerId=customer.customer_id,
                    busId=bus.busId,
                    passangerName=customer.name,
                    bookedSeats=seatsSelected,
                    dateOfJourney=date,
                    isBusRunning=bus.isRunning,
                    operator_id=operator.operator_id,
                    totalFare=bus.fare*len(seatsSelected),
                    isCancelled=False,
                    passangerContact=mobile
                )

                try:
                    ticket.save()
                    bus.bookedSeats = totalBookedSeats
                    bus.save()
                    operator.amountInWallet = operator.amountInWallet+ticket.totalFare
                    operator.save()
                    if gotSeat == False:
                        newSeat = Seats(operator_id=operator.operator_id,
                                        busId=bus.busId, date=date, seatsBooked=seatsSelected)
                        newSeat.save()
                    else:
                        seat = Seats.objects.get(busId=bus.busId, date=date)
                        alreadyBooked = seat.seatsBooked
                        for seats in seatsSelected:
                            alreadyBooked.append(seats)
                        seat.seatsBooked = alreadyBooked
                        seat.save()

                    messages.success(request, "Proceeding to payment..")

                except Exception as e:
                    print(e)
                    messages.warning(
                        request, "Sorry ! Service is unavailable ")

    except Exception as e:
        # give some exception page with nice html here !
        print(e)

    return render(request, "booking.html", context)


def myBookings(request, customerId):
    context = {}
    try:
        customer = Customer.objects.get(customer_id=customerId)
        tickets = Ticket.objects.filter(passengerId=customer.customer_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            operator = Operator.objects.get(operator_id=bus.operator_id)
            bookings.append(Bookings(ticket, customer, bus, operator))

        context['name'] = customer.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['customerId'] = customer.customer_id

        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'myBookings.html', context)


def filterCompleted(request, customerId):
    context = {}
    try:
        customer = Customer.objects.get(customer_id=customerId)
        tickets = Ticket.objects.filter(passengerId=customer.customer_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            operator = Operator.objects.get(operator_id=bus.operator_id)
            booking = Bookings(ticket, customer, bus, operator)
            if booking.isCompleted:
                bookings.append(booking)

        context['name'] = customer.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['customerId'] = customer.customer_id
        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'myBookings.html', context)


def filterCancelled(request, customerId):
    context = {}
    try:
        customer = Customer.objects.get(customer_id=customerId)
        tickets = Ticket.objects.filter(passengerId=customer.customer_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            operator = Operator.objects.get(operator_id=bus.operator_id)
            booking = Bookings(ticket, customer, bus, operator)
            if booking.isTicketCancelled:
                bookings.append(booking)

        context['name'] = customer.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['customerId'] = customer.customer_id
        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'myBookings.html', context)


def filterBooked(request, customerId):
    context = {}
    try:
        customer = Customer.objects.get(customer_id=customerId)
        tickets = Ticket.objects.filter(passengerId=customer.customer_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            operator = Operator.objects.get(operator_id=bus.operator_id)
            booking = Bookings(ticket, customer, bus, operator)
            if booking.isCompleted == False and booking.isTicketCancelled == False:
                bookings.append(booking)

        context['name'] = customer.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['customerId'] = customer.customer_id
        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'myBookings.html', context)


def cancelTicket(request, customerId, ticketId):
    context = {}

    try:

        customer = Customer.objects.get(customer_id=customerId)
        ticket = Ticket.objects.get(ticketId=ticketId)
        operator = Operator.objects.get(operator_id=ticket.operator_id)
        bus = Bus.objects.get(busId=ticket.busId)
        context['booking'] = Bookings(ticket, customer, bus, operator)
        seats = Seats.objects.get(
            busId=ticket.busId, date=ticket.dateOfJourney)
        context['name'] = customer.name
        if request.method == 'POST':
            try:
                operator.amountInWallet = operator.amountInWallet - ticket.totalFare
                operator.cancelledAmount = operator.cancelledAmount + ticket.totalFare
                customer.wallet = customer.wallet + ticket.totalFare

                oldSeats = seats.seatsBooked
                seatUpdate = []
                for seat in seats.seatsBooked:
                    if ticket.bookedSeats.count(seat) == 0:
                        seatUpdate.append(seat)
                seats.seatsBooked = seatUpdate
                ticket.isCancelled = True

                ticket.save()
                operator.save()

                seats.save()
                customer.save()
                messages.success(request, 'Ticket cancelled sucessfully ! ')
                return redirect('/dashboard/mybookings/'+str(customer.customer_id) + '/cancelled')
            except Exception as e:
                print(e)
                messages.warning(
                    request, 'Something failed ! please try later ')

        return render(request, 'cancelTicket.html', context)

    except Exception as e:
        print(e)
        messages.warning(request, 'Something failed ! please try later ')
        return redirect('/dashboard/mybookings/'+str(customer.customer_id))


def userAccount(request, customerId):

    try:

        customer = Customer.objects.get(customer_id=customerId)
        tickets = Ticket.objects.filter(passengerId=customer.customer_id)
        context = {}
        context['name'] = customer.name
        context['customerId'] = customer.customer_id
        context['customer'] = customer
        resultTickets = []
        # edit email

        editEmail = request.POST.get('editEmail')
        if editEmail and editEmail != customer.email:
            customer.email = editEmail
            try:
                customer.save()
                return redirect('/dashboard/account/' + customer.customer_id)
                messages.success(request, "Saved Changes ! ")

            except Exception as e:
                print(e)
                messages.warning('Something failed ! please try again later ')

        # edit email ends here
        try:
            for ticket in tickets:
                # print(ticket)
                bus = Bus.objects.get(busId=ticket.busId)
                operator = Operator.objects.get(operator_id=bus.operator_id)
                # print(ticket, bus, operator)
                resultTickets.append(Bookings(ticket, customer, bus, operator))

        except Exception as e:
            print(e)
        account = UserAcount(customer, resultTickets)
        context['account'] = account
        if len(account.upcommingBookings) > 0:
            context['hasUpcomming'] = True
        else:
            context['hasUpcomming'] = False

        return render(request, 'account.html', context)

    except Exception as e:
        print(e)
        return redirect('/dashboard')
        messages.warning(request, 'something failed ! please try later ')


def contactUs(request, customerId):
    context = {}
    try:
        customer = Customer.objects.get(customer_id=customerId)
        context['name'] = customer.name
        context['customer'] = customer
        context['customerId'] = customer.customer_id

        email = request.POST.get('email')
        query = request.POST.get('query')
        sub = request.POST.get('sub')
        name = request.POST.get('fname')
        if email and query and sub and name:

            subject = 'no-reply bussified customer support '
            message = "Thanks for sending your input ! We will reach you for further help " + \
                "Your Query: " + query
            recepient = str(email)
            try:
                send_mail(subject, message, EMAIL_HOST_USER,
                          [recepient, "ishaan.dwivedi99@gmail.com"], fail_silently=False)

                print("send")
                messages.success(request, "Message Send successfully ! ")
                return redirect('/dashboard')
            except Exception as e:
                messages.warning(
                    request, "Something failed ! Please try again later ")
                print(e)

    except Exception as e:
        messages.warning(request, 'Something failed ! Please try again later ')
        print(e)
    return render(request, 'contactUs.html', context)


def deleteAccount(request, customerId):
    try:
        customer = Customer.objects.get(customer_id=customerId)
        tickets = Ticket.objects.filter(passengerId=customer.customer_id)

        for ticket in tickets:
            if ticket.isCancelled == False:
                thisTicket = Ticket.objects.get(ticketId=ticket.ticketId)
                seats = Seats.objects.get(
                    busId=thisTicket.busId, date=thisTicket.dateOfJourney)
                newSeats = []
                for seat in seats.seatsBooked:
                    if seat in thisTicket.bookedSeats:
                        continue
                    else:
                        newSeats.append(seat)
                seats.seatsBooked = newSeats
                thisTicket.isCancelled = True

                try:
                    thisTicket.save()
                    seats.save()
                except Exception as e:
                    print(e)
                    messages.warning(
                        request, "Something failed ! please try again later ")
                    return redirect('/dashboad')
        customer.delete()
        return redirect('/')

    except Exception as e:
        print(e)
        messages.warning(
            request, "Something failed ! please try again later ")
        return redirect('/dashboard')


def reservations(request, operatorId):
    context = {}
    try:
        operator = Operator.objects.get(operator_id=operatorId)
        tickets = Ticket.objects.filter(operator_id=operator.operator_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            customer = Customer.objects.get(customer_id=ticket.passengerId)
            bookings.append(Bookings(ticket, customer, bus, operator))

        context['name'] = operator.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['operator'] = operator

        context['test'] = 'test'

        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'operatorBookings.html', context)


def operatorFilterCompleted(request, operatorId):

    context = {}
    try:
        operator = Operator.objects.get(operator_id=operatorId)
        tickets = Ticket.objects.filter(operator_id=operator.operator_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            customer = Customer.objects.get(customer_id=ticket.passengerId)
            b = Bookings(ticket, customer, bus, operator)
            if b.isCompleted == True:
                bookings.append(b)

        context['name'] = operator.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['operator'] = operator

        context['test'] = 'test'

        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'operatorBookings.html', context)


def operatorFilterCancelled(request, operatorId):

    context = {}
    try:
        operator = Operator.objects.get(operator_id=operatorId)
        tickets = Ticket.objects.filter(operator_id=operator.operator_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            customer = Customer.objects.get(customer_id=ticket.passengerId)
            b = Bookings(ticket, customer, bus, operator)
            if b.isTicketCancelled == True:
                bookings.append(b)

        context['name'] = operator.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['operator'] = operator

        context['test'] = 'test'

        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'operatorBookings.html', context)


def operatorFilterBooked(request, operatorId):

    context = {}
    try:
        operator = Operator.objects.get(operator_id=operatorId)
        tickets = Ticket.objects.filter(operator_id=operator.operator_id)
        bookings = []

        for ticket in tickets:
            bus = Bus.objects.get(busId=ticket.busId)
            customer = Customer.objects.get(customer_id=ticket.passengerId)
            b = Bookings(ticket, customer, bus, operator)
            if b.isCompleted == False and b.isTicketCancelled == False:
                bookings.append(b)

        context['name'] = operator.name
        context['tickets'] = tickets
        context['bookings'] = bookings
        context['operator'] = operator

        context['test'] = 'test'

        if len(bookings) == 0:
            context['hasNoBookings'] = True
        else:
            context['hasNoBookings'] = False
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'operatorBookings.html', context)


def cancelTicketOperator(request, customerId, ticketId):
    context = {}

    try:

        customer = Customer.objects.get(customer_id=customerId)
        ticket = Ticket.objects.get(ticketId=ticketId)
        operator = Operator.objects.get(operator_id=ticket.operator_id)
        bus = Bus.objects.get(busId=ticket.busId)
        context['booking'] = Bookings(ticket, customer, bus, operator)
        seats = Seats.objects.get(
            busId=ticket.busId, date=ticket.dateOfJourney)
        context['name'] = customer.name
        if request.method == 'POST':
            try:
                operator.amountInWallet = operator.amountInWallet - ticket.totalFare
                operator.cancelledAmount = operator.cancelledAmount + ticket.totalFare
                customer.wallet = customer.wallet + ticket.totalFare

                oldSeats = seats.seatsBooked
                seatUpdate = []
                for seat in seats.seatsBooked:
                    if ticket.bookedSeats.count(seat) == 0:
                        seatUpdate.append(seat)
                seats.seatsBooked = seatUpdate
                ticket.isCancelled = True

                ticket.save()
                operator.save()

                seats.save()
                customer.save()
                messages.success(request, 'Ticket cancelled sucessfully ! ')
                return redirect('/operator/dashboard/bookings/'+str(operator.operator_id) + '/cancelled')
            except Exception as e:
                print(e)
                messages.warning(
                    request, 'Something failed ! please try later ')

        return render(request, 'cancelTicket.html', context)

    except Exception as e:
        print(e)
        messages.warning(request, 'Something failed ! please try later ')
        return redirect('/operator/dashboard/bookings/'+str(operator.operator_id))


def myBusses(request, operatorId):
    context = {}
    try:
        operator = Operator.objects.get(operator_id=operatorId)
        context['operator'] = operator
        context['name'] = operator.name

    except Exception as e:
        print(e)

    return render(request, "mybus.html", context)


def operatorAccount(request, operatorId):

    try:

        operator = Operator.objects.get(operator_id=operatorId)
        tickets = Ticket.objects.filter(operator_id=operator.operator_id)
        context = {}
        context['name'] = operator.name
        context['operatorId'] = operator.operator_id
        context['operator'] = operator
        resultTickets = []
        # edit email

        editEmail = request.POST.get('editEmail')
        if editEmail and editEmail != operator.email:
            customer.email = editEmail
            try:
                customer.save()
                return redirect('/operator/dashboard/account/' + operator.operator_id)
                messages.success(request, "Saved Changes ! ")

            except Exception as e:
                print(e)
                messages.warning('Something failed ! please try again later ')

        # edit email ends here
        try:
            for ticket in tickets:
                # print(ticket)
                bus = Bus.objects.get(busId=ticket.busId)
                customer = Customer.objects.get(customer_id=ticket.passengerId)
                # print(ticket, bus, operator)
                resultTickets.append(Bookings(ticket, customer, bus, operator))

        except Exception as e:
            print(e)
        account = UserAcount(customer, resultTickets)
        context['account'] = account
        if len(account.upcommingBookings) > 0:
            context['hasUpcomming'] = True
        else:
            context['hasUpcomming'] = False

        return render(request, 'account.html', context)

    except Exception as e:
        print(e)
        return redirect('/operator/dashboard')
        messages.warning(request, 'something failed ! please try later ')
