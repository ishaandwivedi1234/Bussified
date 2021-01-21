from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    wallet = models.FloatField(default=0)
    hearts = models.FloatField(default=200)

    def __str__(self):
        return self.name


class Bus(models.Model):

    operator_id = models.CharField(max_length=10000000)
    busId = models.AutoField(primary_key=True)
    busNumber = models.CharField(unique=True, max_length=200)
    busName = models.CharField(unique=True, max_length=200)
    goesfrom = models.CharField(max_length=300)
    goesTo = models.CharField(max_length=300)
    departureTime = models.TimeField()
    arrivalTime = models.TimeField()
    agencyName = models.CharField(max_length=300)
    stops = ArrayField(ArrayField(
        models.CharField(max_length=110, ),)
    )
    seats = models.IntegerField()
    bookedSeats = ArrayField(
        ArrayField(
            models.CharField(max_length=10)
        )
    )
    runsOn = ArrayField(
        ArrayField(
            models.CharField(max_length=100)
        ),
        default=['monday', 'tuesday', 'wednesday',
                 'thursday', 'friday', 'saturday', 'sunday']

    )
    arrivesOnDay = models.IntegerField(default=1)
    fare = models.FloatField()
    stopsFareCutting = models.FloatField()
    hasAc = models.BooleanField()
    isSleeper = models.BooleanField()
    isRunning = models.BooleanField(default=True)

    def __str__(self):
        return self.busName


class Operator(models.Model):
    operator_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    agencyName = models.CharField(max_length=128)
    amountInWallet = models.FloatField(default=0.0)
    cancelledAmount = models.FloatField(default=0.0)
    helpline = models.CharField(max_length=12, default="000-000-000")

    def __str__(self):
        return self.agencyName


class Ticket(models.Model):
    passangerName = models.CharField(max_length=10028)
    passangerContact = models.CharField(max_length=12, default='000-000-000')
    ticketId = models.AutoField(primary_key=True)
    busId = models.CharField(max_length=10028, default='-1')
    passengerId = models.CharField(max_length=10028)
    bookedSeats = ArrayField(
        ArrayField(
            models.CharField(max_length=10)
        )
    )
    totalFare = models.FloatField(default=0.0)
    bookingDate = models.DateTimeField(auto_now_add=True)
    dateOfJourney = models.DateField()
    isBusRunning = models.BooleanField()
    operator_id = models.CharField(max_length=10000)
    isCancelled = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)

    def __str__(self):
        return self.passangerName


class Seats(models.Model):
    busId = models.CharField(max_length=10000)
    operator_id = models.CharField(max_length=10000)
    date = models.DateField(unique=False)
    seatsBooked = ArrayField(
        ArrayField(
            models.CharField(max_length=10)
        )
    )
