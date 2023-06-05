from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('login/', CreateTokenView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('register-staff/', StaffRegistrationView.as_view(), name='staff-registration'),
    
    path('book-queue/', QueueBooking.as_view(), name='queue-booking'),
    path('register-queue/', QueueRegistrationView.as_view(), name='queue-registration'),
    path("queue-detail/", QueueDetailView.as_view(), name="queue-detail"),

    path("center-detail/", CenterDetailView.as_view(), name="center-detail"),

    path("kims-stations/", KimsStationsView.as_view(), name="kims-stations"),
    path("kims-kit/", KimsView.as_view(), name="kims-kit"),

    path('counties/', CountyList.as_view(), name='county-list'),
    path('counties/<int:pk>/', CountyDetail.as_view(), name='county-detail'),

    path('constituencies/', ConstituencyList.as_view(), name='constituency-list'),
    path('constituencies/<int:pk>/', ConstituencyDetail.as_view(), name='constituency-detail'),

    path('wards/', WardList.as_view(), name='ward-list'),
    path('wards/<int:pk>/', WardDetail.as_view(), name='ward-detail'),

    path('polling-centers/', PollingCenterList.as_view(), name='polling-center-list'),
    path('polling-centers/<int:pk>/', PollingCenterDetail.as_view(), name='polling-center-detail'),

    path('polling-stations/', PollingStationList.as_view(), name='polling-station-list'),
    path('polling-stations/<int:pk>/', PollingStationDetail.as_view(), name='polling-station-detail'),

    path('queues/', QueueList.as_view(), name='queue-list'),
    path('queues/<int:pk>/', QueueDetail.as_view(), name='queue-detail'),

    path('voters/', VoterList.as_view(), name='voter-list'),
    path('voters/<int:pk>/', VoterDetail.as_view(), name='voter-detail'),

    path('staffs/', StaffList.as_view(), name='staff-list'),
    path('staffs/<int:pk>/', StaffDetail.as_view(), name='staff-detail'),

    path('tickets/', TicketList.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', TicketDetail.as_view(), name='ticket-detail'),

    path('time-slots/', TimeSlotList.as_view(), name='time-slot-list'),
    path('time-slots/<int:pk>/', TimeSlotDetail.as_view(), name='time-slot-detail'),

    path('votes/', VoteList.as_view(), name='vote-list'),
    path('votes/<int:pk>/', VoteDetail.as_view(), name='vote-detail'),
]
