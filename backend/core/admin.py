from django.contrib import admin
from .models import *

admin.site.register(
    [
        UserProfile,
        Vote,
        Voter,
        PollingStation,
        Queue,
        Ward,
        PollingCenter,
        Constituency,
        County,
        Staff,
        Ticket,
        TimeSlot
    ]
)
