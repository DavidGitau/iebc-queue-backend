from django.db import models
from django.contrib.auth.models import User


class County(models.Model):
    id = models.IntegerField(primary_key=True)                                      #The ID of the station as primary key
    name = models.CharField(max_length=100)                                                 #The name of polling station

    def __str__(self):
        return self.name

class Constituency(models.Model):
    id = models.IntegerField(primary_key=True)                                      #The ID of the station as primary key
    name = models.CharField(max_length=100)                                                 #The name of polling station
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Ward(models.Model):
    id = models.IntegerField(primary_key=True)                                      #The ID of the station as primary key
    name = models.CharField(max_length=100)                                                 #The name of polling station
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, null=True)                                        #Constituency

    def __str__(self):
        return self.name
    
class PollingCenter(models.Model):
    id = models.IntegerField(primary_key=True)                                      #The ID of the station as primary key
    name = models.CharField(max_length=100)                                                  #The list of voters registered in the station
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True)                                                #Ward
    voter_no = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class PollingStation(models.Model):
    id = models.CharField(max_length=50, primary_key=True)                                      #The ID of the station as primary key
    name = models.CharField(max_length=100)                                                #The list of voters registered in the station
    center = models.ForeignKey(PollingCenter, on_delete=models.CASCADE, null=True)                                                #Ward    
    voters = models.ManyToManyField('Voter')                                                #The list of voters registered in the station
    voter_no = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    

class Queue(models.Model):
    name = models.CharField(max_length=100)
    station = models.ForeignKey('PollingStation', on_delete=models.CASCADE, null=True)
    # id = models.IntegerField(primary_key=True)
    tickets = models.ManyToManyField('Ticket', related_name='queues')  # Updated related_name argument

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
    age = models.IntegerField(null=True)                                                             #Age
    dob = models.DateField(null=True)
    first_name = models.CharField(max_length=50)                                            #First name
    gender = models.CharField('gender', max_length=1, choices=GENDER)                       #Gender 
    id_number = models.IntegerField(primary_key=True)                                       #The national ID number used as the primary key 
    last_name = models.CharField(max_length=50)                                             #Last name
    occupation = models.CharField('occupation', max_length=2, choices=OCCUPATION, null=True)           #The occupation of user - casual or formal
    special_condition = models.CharField('condition', max_length=1, choices=CONDITION, null=True)      #Any special condition such as expectant mothers
    user = models.OneToOneField(User, on_delete=models.CASCADE)                             #Used for authetication - django user model

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.id_number}'                     #Return full names with ID number


class Voter(models.Model):
    profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)                 #Connected to a single registered user
    id = models.IntegerField(primary_key=True)                                        #The voter ID number used as the primary key 
    service_time = models.FloatField(default=0.00)                                          #Predicted service time
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, null=True, related_name='ticket')                                 #Queue Ticket number
    voted = models.BooleanField(default=False)                                              #Has voted or not. True or False
    timeslot = models.ForeignKey('TimeSlot', on_delete=models.CASCADE, null=True)
    center = models.ForeignKey('PollingCenter', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.profile} - {self.id}' 

class Staff(models.Model):
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE)                 #Connected to a single registered user
    # id = models.IntegerField(primary_key=True)                                      #The ID of the station as primary key
    center = models.ForeignKey('PollingCenter', on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.first_name


class Vote(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE)                           
    # id = models.IntegerField(primary_key=True)                                         #The voter ID number used as the primary key 
    station = models.ForeignKey('PollingStation', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.voter} - {self.id}' 
    

class Ticket(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE, related_name='voter')                           
    station = models.ForeignKey('PollingStation', on_delete=models.CASCADE, null=True)
    # id = models.IntegerField(primary_key=True)                                         #The voter ID number used as the primary key 

    def __str__(self):
        return f'{self.voter} - {self.id}' 
    
class TimeSlot(models.Model):                         
    id = models.IntegerField(primary_key=True)                                         #The voter ID number used as the primary key 
    start = models.TimeField()
    stop = models.TimeField()
    voters = models.ManyToManyField('Voter', related_name='voters')  

    def __str__(self):
        return f'{self.start} - {self.stop}' 