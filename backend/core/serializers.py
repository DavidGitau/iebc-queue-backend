from rest_framework import serializers
from core.models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class VoterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = Voter
        fields = '__all__'

class PollingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollingStation
        fields = '__all__'

class QueueSerializer(serializers.ModelSerializer):
    station = PollingStationSerializer()

    class Meta:
        model = Queue
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    voter = VoterSerializer()

    class Meta:
        model = Vote
        fields = '__all__'
