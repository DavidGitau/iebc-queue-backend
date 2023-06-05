from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from .models import *
from .serializers import *
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
# from .serializers import StaffRegistrationSerializer

class QueueDetailView(APIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cid = request.data['cid']
        try:
            c = PollingCenter.objects.get(id=cid)
            try:
                s = PollingStation.objects.filter(center=c)[0]
                q = Queue.objects.get(station=s)
                serializer = QueueSerializer(q)
                return Response(serializer.data)
            except:
                return Response({'error': f'Queue for {c.name} not found!'}, status=404)
        except:
            return Response({'error': f'Center not found!'}, status=404)

class CenterDetailView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cid = request.data['cid']
        try:
            c = PollingCenter.objects.get(id=cid)
            try:
                s = Voter.objects.filter(center=c)
                serializer = VoterSerializer(s, many=True)
                return Response(serializer.data)
            except:
                return Response({'error': f'Voters for {c.name} not found!'}, status=404)
        except:
            return Response({'error': f'Center not found!'}, status=404)
        

class KimsStationsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = PollingStationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cid = request.data['cid']
        try:
            c = PollingCenter.objects.get(id=cid)
            try:
                s = PollingStation.objects.filter(center=c)
                serializer = PollingStationSerializer(s, many=True)
                return Response(serializer.data)
            except:
                return Response({'error': f'Stations for {c.name} not found!'}, status=404)
        except:
            return Response({'error': f'Center not found!'}, status=404)


class KimsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vid = request.data['id']
        sid = request.data['sid']
        voter = Voter.objects.get(profile__id_number=vid)
        print(voter)
        try:
            ticket  = voter.ticket
            if int(ticket.station.id) == int(sid):
                q = Queue.objects.get(station=ticket.station)
                if ticket in q.tickets.all():
                    q.tickets.remove(ticket)
                    q.save()
                    voter.voted = True
                    voter.save()
                    Vote.objects.create(voter=voter, station=ticket.station)
                    return Response()
                else:
                    return Response({'error': f'Already voter has casted their vote!'}, status=404)
            else:
                return Response({'error': f'Wrong station. Please proceed to {ticket.station.name} {ticket.station.id}'}, status=404)
        except:
            return Response({'error': f'Register to queue first! Ticket not found!'}, status=404)

class QueueRegistrationView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vid = request.data['id']
        cid = request.data['cid']
        try:
            voter = Voter.objects.get(profile__id_number=vid)
            center  = voter.center
            if center.id == int(cid):
                try: 
                    t = Ticket.objects.get(voter=voter)
                    return Response({'error': f'Voter has a ticket already - number {t.id}'}, status=404)
                except:
                    s = PollingStation.objects.filter(center=center)[0]
                    ticket = Ticket.objects.create(voter=voter,station=s)
                    q = Queue.objects.get(station=s)
                    q.tickets.add(ticket)
                    q.save()
                    print(q.tickets.all())
                    voter.ticket = ticket
                    voter.save()
                    return Response()
            else:
                return Response({'error': f'Voter not found in this center! Proceed to {center.name} '}, status=404)
        except:
            return Response({'error': f'Voter not found! Ensure you are a registered voter! '}, status=404)

class QueueBooking(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tid = request.data['timeslot']
        vid = request.data['id']
        timeslot = TimeSlot.objects.get(id=tid)
        voter = Voter.objects.get(id=vid)
        voter.timeslot = timeslot
        voter.save()
        return Response()
        

class StaffRegistrationView(APIView):
    queryset = Staff.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StaffRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save()
            return Response({'message': 'Staff registration successful.', 'staff_id': staff.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(ObtainAuthToken):
    def post(self, request):
        # Delete the user's authentication token
        Token.objects.filter(user=request.user).delete()
        return Response({'detail': 'Logged out successfully'})


class CustomList(generics.ListCreateAPIView):
    pass


class CustomDetail(generics.RetrieveDestroyAPIView):
    pass


class ProfileAPIView(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            # print(request.user.username)
            try:
                staff = Staff.objects.get(profile=profile)
                serializer = StaffSerializer(staff)
            except:
                try:
                    voter = Voter.objects.get(profile=profile)
                    serializer = VoterSerializer(voter)
                except: 
                    serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=404)

class CreateTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Logout any authenticated user
        logout(request)
        
        try:
            # Check the user's account type
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Handle different account types
            if user.is_superuser:
                if request.data['group'] == 'admin':
                    # Perform user-specific authentication logic
                    print(user,'admin')
                    return Response({'token': token.key, 'account_type': 'admin'})
                else:
                    return Response({'detail': 'Invalid account type - Got admin details'}, status=400)
            elif user.is_staff:
                if request.data['group'] == 'admin':
                    # Perform user-specific authentication logic
                    print(user,'staff')
                    return Response({'token': token.key, 'account_type': 'staff'})
                else:
                    return Response({'detail': 'Invalid account type - Got staff details'}, status=400)
            else:
                if request.data['group'] == 'user':
                    # Perform admin-specific authentication logic
                    profile = UserProfile.objects.get(user=user)
                    voter = Voter.objects.get(profile=profile)
                    return Response({'token': token.key, 'account_type': 'user', 'voter_id': voter.id})
                else:
                    return Response({'detail': 'Invalid account type - Got voter details'}, status=400)
        except:
            return Response({'detail': 'Invalid password or username'}, status=400)


class CountyList(generics.ListCreateAPIView):
    queryset = County.objects.all()[:50]
    serializer_class = CountySerializer


class CountyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = County.objects.all()[:50]
    serializer_class = CountySerializer


class ConstituencyList(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()[:50]
    serializer_class = ConstituencySerializer


class ConstituencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()[:50]
    serializer_class = ConstituencySerializer


class WardList(generics.ListCreateAPIView):
    queryset = Ward.objects.all()[:50]
    serializer_class = WardSerializer


class WardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ward.objects.all()[:50]
    serializer_class = WardSerializer


class PollingCenterList(generics.ListCreateAPIView):
    queryset = PollingCenter.objects.all()[:50]
    serializer_class = PollingCenterSerializer


class PollingCenterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PollingCenter.objects.all()[:50]
    serializer_class = PollingCenterSerializer


class PollingStationList(generics.ListCreateAPIView):
    queryset = PollingStation.objects.all()[:50]
    serializer_class = PollingStationSerializer


class PollingStationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PollingStation.objects.all()[:50]
    serializer_class = PollingStationSerializer


class QueueList(generics.ListCreateAPIView):
    queryset = Queue.objects.all()[:50]
    serializer_class = QueueSerializer


class QueueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Queue.objects.all()[:50]
    serializer_class = QueueSerializer


class VoterList(generics.ListCreateAPIView):
    queryset = Voter.objects.all()[:50]
    serializer_class = VoterSerializer


class VoterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voter.objects.all()[:50]
    serializer_class = VoterSerializer


class StaffList(generics.ListCreateAPIView):
    queryset = Staff.objects.all()[:50]
    serializer_class = StaffSerializer


class StaffDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()[:50]
    serializer_class = StaffSerializer


class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()[:50]
    serializer_class = TicketSerializer


class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()[:50]
    serializer_class = TicketSerializer


class TimeSlotList(generics.ListCreateAPIView):
    queryset = TimeSlot.objects.all()[:50]
    serializer_class = TimeSlotSerializer


class TimeSlotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeSlot.objects.all()[:50]
    serializer_class = TimeSlotSerializer


class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()[:50]
    serializer_class = VoteSerializer


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()[:50]
    serializer_class = VoteSerializer
