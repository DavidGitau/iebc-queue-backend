from django.db import models
from django.contrib.auth.models import User


class PollingStation(models.Model):
    station_id = models.IntegerField(primary_key=True)                                      #The ID of the station as primary key
    name = models.CharField(max_length=100)                                                 #The name of polling station
    location = models.CharField(max_length=100)                                             #The center the station is located
    voters = models.ManyToManyField('Voter')                                                #The list of voters registered in the station
    scounty = models.CharField(max_length=100)                                              #County
    sconstituency = models.CharField(max_length=100)                                        #Constituency
    sward = models.CharField(max_length=100)                                                #Ward

    def __str__(self):
        return self.name
    

class Queue(models.Model):
    name = models.CharField(max_length=100)                                                 #Queue name
    length = models.IntegerField()                                                          #Numbers of voters in queue
    station = models.ForeignKey('PollingStation', on_delete=models.CASCADE)                 #The polling station queue is located in
    queue_id = models.IntegerField(primary_key=True)                                        #The ID of the queue as primary key
    voters = models.ManyToManyField('Voter')                                                #List of all voters in the queue

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    # Choices
    CONDITION = (
        ("E", "Expectant/Mothers"),
        ("S", "Sick"),
        ("D", "Disabled"),
        ("N", "None"),
    )
    GENDER = (
        ("M", "Male"),
        ("F", "Female"),
    )
    OCCUPATION = (
        ("C", "Casual"),
        ("F", "Formal"),
    )

    # Fields/Attributes
    age = models.IntegerField()                                                             #Age
    first_name = models.CharField(max_length=50)                                            #First name
    gender = models.CharField('gender', max_length=1, choices=GENDER)                       #Gender 
    id_number = models.IntegerField(primary_key=True)                                       #The national ID number used as the primary key     
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')              #Picture of user
    last_name = models.CharField(max_length=50)                                             #Last name
    occupation = models.CharField('occupation', max_length=1, choices=OCCUPATION)           #The occupation of user - casual or formal
    special_condition = models.CharField('condition', max_length=1, choices=CONDITION)      #Any special condition such as expectant mothers
    user = models.OneToOneField(User, on_delete=models.CASCADE)                             #Used for authetication - django user model

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.id_number}'                     #Return full names with ID number


class Voter(models.Model):
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE)                 #Connected to a single registered user
    voter_id = models.IntegerField(primary_key=True)                                        #The voter ID number used as the primary key 
    service_time = models.FloatField(default=0.00)                                          #Predicted service time
    waiting_time = models.FloatField(default=0.00)                                          #Predicted time on queue
    ticket_no = models.CharField(max_length=500, null=True)                                 #Queue Ticket number
    voted = models.BooleanField(default=False)                                              #Has voted or not. True or False

    def __str__(self):
        return f'{self.profile} - {self.voter_id}' 


class Vote(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE)                           
    vote_id = models.IntegerField(primary_key=True)                                         #The voter ID number used as the primary key 

    def __str__(self):
        return f'{self.voter} - {self.vote_id}' 