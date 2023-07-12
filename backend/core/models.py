from django.db import models
from django.contrib.auth.models import User

class County(models.Model):
    id = models.IntegerField(primary_key=True)  # The ID of the station as primary key
    name = models.CharField(max_length=100)  # The name of the polling station

    def __str__(self):
        return self.name

class Constituency(models.Model):
    id = models.IntegerField(primary_key=True)  # The ID of the station as primary key
    name = models.CharField(max_length=100)  # The name of the polling station
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True)  # Belongs to a County

    def __str__(self):
        return self.name

class Ward(models.Model):
    id = models.IntegerField(primary_key=True)  # The ID of the station as primary key
    name = models.CharField(max_length=100)  # The name of the polling station
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null=True)  # Belongs to a Constituency

    def __str__(self):
        return self.name

class PollingCenter(models.Model):
    id = models.IntegerField(primary_key=True)  # The ID of the station as primary key
    name = models.CharField(max_length=100)  # The list of voters registered in the station
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True)  # Belongs to a Ward
    voter_no = models.IntegerField(default=0)  # Number of voters registered in the center

    def __str__(self):
        return self.name

class PollingStation(models.Model):
    id = models.CharField(max_length=50, primary_key=True)  # The ID of the station as primary key
    name = models.CharField(max_length=100)  # The list of voters registered in the station
    center = models.ForeignKey(PollingCenter, on_delete=models.SET_NULL, null=True)  # Belongs to a Polling Center
    voters = models.ManyToManyField('Voter')  # The list of voters registered in the station
    voter_no = models.IntegerField(default=1)  # Number of voters registered in the station

    def __str__(self):
        return self.name

class Queue(models.Model):
    name = models.CharField(max_length=100)
    station = models.ForeignKey('PollingStation', on_delete=models.SET_NULL, null=True)  # Belongs to a Polling Station
    waiting_time = models.FloatField(default=0.00)  # Waiting time in the queue
    current_voter_st = models.FloatField(default=0.00)  # Current voter's service time
    tickets = models.ManyToManyField('Ticket', related_name='queues')  # Tickets associated with the queue

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # Choices
    CONDITION = (
        ("S", "Special"),
        ("N", "None"),
    )
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )
    OCCUPATION = (
        ("CH", "Casual Hard"),
        ("CS", "Casual Soft"),
        ("F", "Formal"),
    )

    # Fields/Attributes
    age = models.IntegerField(null=True)  # Age of the user
    dob = models.DateField(null=True)  # Date of birth
    first_name = models.CharField(max_length=50)  # First name of the user
    gender = models.CharField('gender', max_length=1, choices=GENDER)  # Gender of the user
    id_number = models.IntegerField(primary_key=True)  # National ID number used as primary key
    last_name = models.CharField(max_length=50)  # Last name of the user
    occupation = models.CharField('occupation', max_length=2, choices=OCCUPATION, null=True)  # Occupation of the user
    special_condition = models.CharField('condition', max_length=1, choices=CONDITION, null=True)  # Special condition of the user
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)  # Django user model for authentication

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.id_number}'  # Return full names with ID number

class Voter(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True)  # Connected to a single registered user
    id = models.IntegerField(primary_key=True)  # Voter ID number used as primary key
    service_time = models.FloatField(default=0.00)  # Predicted service time
    ticket = models.ForeignKey('Ticket', on_delete=models.SET_NULL, null=True, related_name='ticket')  # Queue ticket number
    voted = models.BooleanField(default=False)  # Has the voter voted or not
    timeslot = models.ForeignKey('TimeSlot', on_delete=models.SET_NULL, null=True)  # Time slot assigned to the voter
    center = models.ForeignKey('PollingCenter', on_delete=models.SET_NULL, null=True)  # Belongs to a Polling Center

    def __str__(self):
        return f'{self.profile} - {self.id}'  # Return user profile and ID

class Staff(models.Model):
    profile = models.OneToOneField('UserProfile', on_delete=models.SET_NULL, null=True)  # Connected to a single registered user
    center = models.ForeignKey('PollingCenter', on_delete=models.SET_NULL, null=True)  # Belongs to a Polling Center

    def __str__(self):
        return self.profile.first_name  # Return staff's first name

class Vote(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.SET_NULL, null=True)  # Belongs to a Voter
    station = models.ForeignKey('PollingStation', on_delete=models.SET_NULL, null=True)  # Belongs to a Polling Station

    def __str__(self):
        return f'{self.voter} - {self.id}'  # Return voter and ID

class Ticket(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.SET_NULL, related_name='voter', null=True)  # Belongs to a Voter
    station = models.ForeignKey('PollingStation', on_delete=models.SET_NULL, null=True)  # Belongs to a Polling Station
    queue_number = models.IntegerField(default=1)  # Queue number of the ticket
    priority = models.IntegerField(default=1)  # Priority of the ticket
    waiting_time = models.FloatField(default=0.00)  # Waiting time for the ticket
    CONDITION = (
        ("S", "Special"),
        ("A", "On Time"),
        ("B", "Out of Time"),
    )
    type = models.CharField('condition', max_length=1, choices=CONDITION)  # Condition/type of the ticket
    active = models.BooleanField(default=True) 

    def __str__(self):
        return f'{self.voter} - {self.id}'  # Return voter and ID

class TimeSlot(models.Model):                         
    id = models.IntegerField(primary_key=True)  # The voter ID number used as the primary key
    start = models.TimeField()  # Start time of the time slot
    stop = models.TimeField()  # Stop time of the time slot
    voters = models.ManyToManyField('Voter', related_name='voters')  # Voters assigned to the time slot

    def __str__(self):
        return f'{self.start} - {self.stop}'  # Return start and stop times of the time slot
