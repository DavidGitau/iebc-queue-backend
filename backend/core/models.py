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
    length = models.IntegerField()
    station = models.ForeignKey('PollingStation', on_delete=models.CASCADE, null=True)
    id = models.IntegerField(primary_key=True)
    voters = models.ManyToManyField('Voter', related_name='queues')  # Updated related_name argument

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
    age = models.IntegerField(null=True)                                                             #Age
    dob = models.DateField(null=True)
    first_name = models.CharField(max_length=50)                                            #First name
    gender = models.CharField('gender', max_length=1, choices=GENDER)                       #Gender 
    id_number = models.IntegerField(primary_key=True)                                       #The national ID number used as the primary key 
    last_name = models.CharField(max_length=50)                                             #Last name
    occupation = models.CharField('occupation', max_length=1, choices=OCCUPATION)           #The occupation of user - casual or formal
    special_condition = models.CharField('condition', max_length=1, choices=CONDITION, null=True)      #Any special condition such as expectant mothers
    user = models.OneToOneField(User, on_delete=models.CASCADE)                             #Used for authetication - django user model

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.id_number}'                     #Return full names with ID number


class Voter(models.Model):
    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE)                 #Connected to a single registered user
    id = models.IntegerField(primary_key=True)                                        #The voter ID number used as the primary key 
    service_time = models.FloatField(default=0.00)                                          #Predicted service time
    waiting_time = models.FloatField(default=0.00)                                          #Predicted time on queue
    ticket_no = models.CharField(max_length=500, null=True)                                 #Queue Ticket number
    voted = models.BooleanField(default=False)                                              #Has voted or not. True or False
    station = models.ForeignKey('PollingStation', on_delete=models.CASCADE, null=True)
    queue = models.ForeignKey('Queue', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f'{self.profile} - {self.id}' 


class Vote(models.Model):
    voter = models.ForeignKey('Voter', on_delete=models.CASCADE)                           
    vote_id = models.IntegerField(primary_key=True)                                         #The voter ID number used as the primary key 

    def __str__(self):
        return f'{self.voter} - {self.vote_id}' 
    