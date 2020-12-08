from django.shortcuts import render, redirect
from home.models import Customer, Bus, Operator, Ticket
from django.contrib import messages
from datetime import datetime
from home.custom_models import Result, Bookings

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
        customer = Customer(name=name, email=email, password=password)

        try:
            customer.save()
            messages.success(
                request, "You have sucessfully registered with Bussified ! ")
            print("saved to database")

        except:
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
            messages.success(
                request, "You have sucessfully registered with Bussified ! ")
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
                for b in bus:
                    if dayOfJourney in b.runsOn:
                        print(b.bookedSeats)
                        print("match")
                        resultsForDay.append(Result(b))
                    else:
                        resultsForNonDays.append(Result(b))

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

        context['name'] = customer.name
        context['bus'] = Result(bus)
        context['customer'] = customer
        context['dateOfJourney'] = date

        # booking logic
        seatsSelected = request.POST.getlist('seatsSelected')
        print(bus.bookedSeats)

        mobile = request.POST.get('mobile')

        if mobile:
            if len(seatsSelected) == 0:
                messages.warning(
                    request, "Please select atleast 1 seat to book a ticket !")
            else:
                totalBookedSeats = []
                for seats in bus.bookedSeats:
                    totalBookedSeats.append(seats)
                for seats in seatsSelected:
                    totalBookedSeats.append(seats)

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
                )

                try:
                    ticket.save()
                    bus.bookedSeats = totalBookedSeats
                    bus.save()
                    operator.amountInWallet = operator.amountInWallet+ticket.totalFare
                    operator.save()
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
    except Exception as e:
        print(e)
        messages.warning(request, "Please log in to your accouont ! ")
    return render(request, 'myBookings.html', context)
