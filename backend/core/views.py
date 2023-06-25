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

import random
import datetime
from django.db.models import F, Case, When, IntegerField, Value, Sum, ExpressionWrapper, DecimalField
from decimal import Decimal, ROUND_DOWN

def re_render_queue(q):
    # Recalculate the queue priority for all tickets in the queue
    priority_expression = Case(
        When(type='S', then=Value(1)),
        When(type='A', then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
    q.tickets.update(priority=priority_expression)

    # Reassign ticket numbers based on the recalculated priority and earlier ID for the same priority
    tickets = q.tickets.order_by('priority', 'id')
    waiting_time = Decimal(0).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    previous_service_time = Decimal(q.current_voter_st).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

    for index, ticket in enumerate(tickets):
        ticket.queue_number = index + 1
        waiting_time = waiting_time + previous_service_time
        ticket.waiting_time = waiting_time.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        ticket.save()

        # Update the waiting time for the next ticket
        previous_service_time = Decimal(ticket.voter.service_time).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

    wt = Decimal(q.tickets.aggregate(total_time=Sum('voter__service_time'))['total_time'] or 0)
    q.waiting_time = (wt + Decimal(q.current_voter_st)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    q.save()


class DisallocateTimeslotsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cid = request.data['cid']
        try:
            center = PollingCenter.objects.get(id=cid)
            voters = Voter.objects.filter(center=center)
            for voter in voters:
                voter.timeslot = None
                voter.save()

        except PollingCenter.DoesNotExist:
            return Response({'error': 'Center not found!'}, status=404)


class AllocateTimeslotsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cid = request.data['cid']
        try:
            center = PollingCenter.objects.get(id=cid)
            while True:
            # Find voters in the center without timeslots
                voters_without_timeslots = Voter.objects.filter(center=center, timeslot=None)
                if len(voters_without_timeslots) == 0:
                    break
                # Shuffle the voters
                shuffled_voters = list(voters_without_timeslots)
                random.shuffle(shuffled_voters)

                # Get all available timeslots sorted by id
                timeslots = TimeSlot.objects.all().order_by('id')

                # Randomly allocate timeslots to voters while ensuring service times do not exceed 60
                allocated_voters = []
                total_service_time = 0

                for voter in shuffled_voters:
                    if not timeslots.exists():
                        break

                    # Randomly select a timeslot
                    selected_timeslot = timeslots.first()
                    total_time = Voter.objects.filter(timeslot=selected_timeslot, center=voter.center).aggregate(total_time=Sum('service_time'))['total_time']

                    try:
                        if total_time >= 60:
                            continue
                    except:
                        pass

                    # Calculate the voter's service time
                    service_time = voter.service_time

                    # Check if adding the service time exceeds the limit
                    if total_service_time + service_time > 60:
                        break

                    # Assign the timeslot to the voter
                    voter.timeslot = selected_timeslot
                    voter.save()

                    # Update total service time
                    total_service_time += service_time

                    allocated_voters.append(voter)
                    timeslots = timeslots.exclude(id=selected_timeslot.id)

            # Serialize the allocated voters
            # serializer = VoterSerializer(allocated_voters, many=True)
            return Response()

        except PollingCenter.DoesNotExist:
            return Response({'error': 'Center not found!'}, status=404)




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
                # s = PollingStation.objects.filter(center=c)
                q = Queue.objects.filter(station__center=c)
                serializer = QueueSerializer(q, many=True)
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
        # vid = request.data['id']
        sid = request.data['sid']
        queue = Queue.objects.get(station__id=int(sid))
        # voter = Voter.objects.get(profile__id_number=vid)
        try:
            ticket = queue.tickets.order_by('queue_number')[0]
            voter = ticket.voter
            # print(voter)
            try:
                # ticket  = voter.ticket
                if int(ticket.station.id) == int(sid):
                    q = Queue.objects.get(station=ticket.station)
                    if ticket in q.tickets.all():
                        # q.tickets.remove(ticket)
                        qw = q.waiting_time - voter.service_time
                        q.waiting_time = qw
                        q.current_voter_st = voter.service_time
                        if q.waiting_time < 0.10:
                            q.waiting_time = 0.00
                        ticket.delete()
                        q.save()
                        re_render_queue(q)
                        # print('iiiiii')
                        try:
                            voter.voted = True
                            print('iiiiii', voter)
                            Vote.objects.create(voter=voter, station=ticket.station)
                            voter.save()
                            print('iiiiii')
                            return Response({'success': f'Ticket {ticket.id} {voter.profile.first_name} {voter.profile.last_name} - {voter.profile.id_number} has casted their vote!'}, status=200)
                        except Exception as e:
                            raise e
                    else:
                        return Response({'error': f'Already voter has casted their vote!'}, status=404)
                else:
                    return Response({'error': f'Wrong station. Please proceed to {ticket.station.name} {ticket.station.id}'}, status=404)
            except:
                return Response({'error': f'Register to queue first! Ticket not found!'}, status=404)
        except:
            return Response({'error': f'Queue Empty!'}, status=404)


class QueueRegistrationView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vid = request.data['id']
        cid = request.data['cid']
        sp = request.data['special']
        try:
            voter = Voter.objects.get(profile__id_number=vid)
            center = voter.center
            print(voter, center.id, cid, sp)
            if center.id == int(cid):
                try:
                    try:
                        t = Ticket.objects.get(voter=voter)
                        return Response({'error': f'Voter has a ticket already - number {t.id}'}, status=404)
                    except:
                        s = PollingStation.objects.filter(center=center)
                        queues = Queue.objects.filter(station__in=s)
                        for q in queues:
                            q.waiting_time = Decimal(q.tickets.aggregate(total_time=Sum('voter__service_time'))['total_time'] or 0)
                            q.save()
                        q1 = queues.order_by('waiting_time')
                        q = q1.first() if queues.exists() else None
                        total_service_time = q.waiting_time

                        current_time = datetime.datetime.now().time()
                        ticket_type = 'S' if sp else ('A' if voter.timeslot is not None and (voter.timeslot.start <= current_time <= voter.timeslot.stop) else 'B')
                        ticket = Ticket.objects.create(
                            voter=voter,
                            station=q.station,
                            waiting_time=total_service_time,
                            type=ticket_type,
                            queue_number=1,
                        )
                        q.tickets.add(ticket)

                        re_render_queue(q)
                        q.save()

                        voter.ticket = ticket
                        voter.save()

                        return Response({'success': f'Ticket {voter.ticket.id} for {voter.profile.first_name} {voter.profile.last_name} generated successfully'}, status=200)
                except Exception as e:
                    print(e)
                    return Response({'error': f'{e} '}, status=404)
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

        # Calculate the total service time for voters in the same timeslot and center
        total_service_time = Voter.objects.filter(timeslot=timeslot, center=voter.center).aggregate(total_time=Sum('service_time'))['total_time']
        if total_service_time is None:
            total_service_time = 0.0

        # Check if adding the service time of the current voter exceeds 60
        if total_service_time + voter.service_time > 60:
            # Handle the case when the total service time exceeds 60 (e.g., return an error response)
            return Response({"error": "Timeslot already full!"})

        # Save the changes to the voter
        voter.save()

        return Response({"success": f"Booking for {timeslot} sucessful"})

        

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
            print(request.data)
            serializer = self.serializer_class(data=request.data)
            print(serializer)
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
