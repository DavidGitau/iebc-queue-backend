from django.urls import path
from .models import *
from .serializers import *
from .views import *

urlpatterns = [
    path(
        'userprofiles',
        CustomList.as_view(
            queryset=UserProfile.objects.all(),
            serializer_class=UserProfileSerializer
        )
    ),
    path(
        'voters',
        CustomList.as_view(
            queryset=Voter.objects.all(),
            serializer_class=VoterSerializer
        )
    ),
    path(
        'votes',
        CustomList.as_view(
            queryset=Vote.objects.all(),
            serializer_class=VoteSerializer
        )
    ),
    path(
        'queues',
        CustomList.as_view(
            queryset=Queue.objects.all(),
            serializer_class=QueueSerializer
        )
    ),
    path(
        'stations',
        CustomList.as_view(
            queryset=PollingStation.objects.all(),
            serializer_class=PollingStationSerializer
        )
    ),

    # path(
    #     'userprofiles',
    #     CustomList.as_view(
    #         queryset=UserProfile.objects.all(),
    #         serializer_class=UserProfileSerializer
    #     )
    # ),
    # path(
    #     'voters',
    #     CustomList.as_view(
    #         queryset=Voter.objects.all(),
    #         serializer_class=VoterSerializer
    #     )
    # ),
    # path(
    #     'votes',
    #     CustomList.as_view(
    #         queryset=Vote.objects.all(),
    #         serializer_class=VoteSerializer
    #     )
    # ),
    # path(
    #     'queues',
    #     CustomList.as_view(
    #         queryset=Queue.objects.all(),
    #         serializer_class=QueueSerializer
    #     )
    # ),
    path(
        'station/<slug:pk>',
        CustomDetail.as_view(
            queryset=PollingStation.objects.all(),
            serializer_class=PollingStationSerializer
        )
    ),
]