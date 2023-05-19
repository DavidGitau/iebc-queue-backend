from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from core.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('password', 'username')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        style={'input_type': 'text'},
        trim_whitespace=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    # id_number = serializers.IntegerField(read_only=True)
    # gender = serializers.ChoiceField(choices=UserProfile.GENDER)
    user = UserSerializer()

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

