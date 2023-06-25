from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from core.models import *


class StaffRegistrationSerializer(serializers.ModelSerializer):
    id_number = serializers.IntegerField()
    dob = serializers.DateField()
    center_id = serializers.IntegerField()

    class Meta:
        model = Staff
        fields = ['id_number', 'dob', 'center_id']

    def create(self, validated_data):
        id_number = validated_data['id_number']
        dob = validated_data['dob']
        center_id = validated_data['center_id']
        print(id_number,dob,center_id)
        
        try:
            # Retrieve the UserProfile based on id_number
            user_profile = UserProfile.objects.get(id_number=id_number)
            print(user_profile)
            
            # Retrieve the User object based on the UserProfile
            user = user_profile.user
            
            # Set the is_staff field to True
            user.is_staff = True
            user.save()
            
            # Retrieve the PollingCenter based on center_id
            center = PollingCenter.objects.get(id=center_id)
            print(center)
            
            # Create Staff object and associate it with the center
            staff = Staff.objects.create(
                profile=user_profile,
                center=center
            )
            
            return staff
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError('User profile not found.')
        except PollingCenter.DoesNotExist:
            raise serializers.ValidationError('Polling center not found.')


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
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'


class ConstituencySerializer(serializers.ModelSerializer):
    county = CountySerializer()

    class Meta:
        model = Constituency
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    constituency = ConstituencySerializer()

    class Meta:
        model = Ward
        fields = '__all__'


class PollingCenterSerializer(serializers.ModelSerializer):
    ward = WardSerializer()

    class Meta:
        model = PollingCenter
        fields = '__all__'


class PollingStationSerializer(serializers.ModelSerializer):
    center = PollingCenterSerializer()

    class Meta:
        model = PollingStation
        fields = '__all__'




class StaffSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    center = PollingCenterSerializer()

    class Meta:
        model = Staff
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


class VoterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    center = PollingCenterSerializer()
    # ticket = TicketSerializer()
    timeslot = TimeSlotSerializer()

    class Meta:
        model = Voter
        fields = '__all__'

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    station = PollingStationSerializer()
    voter = VoterSerializer()
    type = TicketTypeSerializer()
    
    class Meta:
        model = Ticket
        fields = '__all__'

class QueueSerializer(serializers.ModelSerializer):
    station = PollingStationSerializer()
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Queue
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    voter = VoterSerializer()

    class Meta:
        model = Vote
        fields = '__all__'
