from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import logout
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
import random
import datetime
from django.db.models import Case, When, IntegerField, Value, Sum
from decimal import Decimal, ROUND_DOWN
from django.core.exceptions import ObjectDoesNotExist

def re_render_queue(q):
    try:
        update_ticket_priorities(q)
        reassign_ticket_numbers(q)
        update_waiting_times(q)
    except ObjectDoesNotExist:
        handle_object_does_not_exist_error()
    except Exception as e:
        handle_unexpected_error(e)

def update_ticket_priorities(q):
    priority_expression = Case(
        When(type='S', then=Value(1)),
        When(type='A', then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
    q.tickets.update(priority=priority_expression)

def reassign_ticket_numbers(q):
    tickets = q.tickets.order_by('priority', 'id')
    waiting_time = Decimal(0).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    previous_service_time = Decimal(q.current_voter_st).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

    for index, ticket in enumerate(tickets):
        ticket.queue_number = index + 1
        waiting_time = waiting_time + previous_service_time
        ticket.waiting_time = waiting_time.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        ticket.save()
        previous_service_time = Decimal(ticket.voter.service_time).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

def update_waiting_times(q):
    wt = Decimal(q.tickets.aggregate(total_time=Sum('voter__service_time'))['total_time'] or 0)
    q.waiting_time = (wt + Decimal(q.current_voter_st)).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    q.save()

def handle_object_does_not_exist_error():
    print("Object does not exist error occurred during queue re-rendering.")
    # Raise a custom exception or perform necessary actions

def handle_unexpected_error(exception):
    print(f"An error occurred during queue re-rendering: {str(exception)}")
    # Raise a custom exception or perform necessary actions


class DisallocateTimeslotsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cid = request.data['cid']
            center = PollingCenter.objects.get(id=cid)
            voters = Voter.objects.filter(center=center)

            if voters.exists():
                # Disallocate timeslots for all voters in the center
                for voter in voters:
                    voter.timeslot = None
                    voter.save()

                return Response({'success': 'Timeslots deallocated successfully.'})

            else:
                return Response({'error': 'No voters found in the center.'}, status=404)

        except ObjectDoesNotExist:
            return Response({'error': 'Center not found.'}, status=404)

        except KeyError:
            return Response({'error': 'Invalid request. Missing "cid" parameter.'}, status=400)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)


class AllocateTimeslotsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cid = request.data['cid']
            center = self.get_polling_center(cid)

            voters_without_timeslots = self.get_voters_without_timeslots(center)
            if not voters_without_timeslots:
                return Response({'message': 'No voters without timeslots found.'})

            shuffled_voters = self.shuffle_voters(voters_without_timeslots)
            timeslots = self.get_available_timeslots()
            if not timeslots:
                return Response({'error': 'No available timeslots.'}, status=404)

            allocated_voters = self.allocate_timeslots(shuffled_voters, timeslots, center)
            if allocated_voters:
                return Response({'success': 'Timeslots allocated successfully.'})
            else:
                return Response({'error': 'Unable to allocate timeslots.'}, status=500)

        except ObjectDoesNotExist:
            return Response({'error': 'Center not found.'}, status=404)

        except KeyError:
            return Response({'error': 'Invalid request. Missing "cid" parameter.'}, status=400)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    def get_polling_center(self, cid):
        try:
            return PollingCenter.objects.get(id=cid)
        except PollingCenter.DoesNotExist:
            raise ObjectDoesNotExist('Center not found.')

    def get_voters_without_timeslots(self, center):
        return Voter.objects.filter(center=center, timeslot=None)

    def shuffle_voters(self, voters):
        shuffled_voters = list(voters)
        random.shuffle(shuffled_voters)
        return shuffled_voters

    def get_available_timeslots(self):
        timeslots = list(TimeSlot.objects.all().order_by('id'))
        random.shuffle(timeslots)
        return timeslots[:5]

    def allocate_timeslots(self, voters, timeslots, center):
        allocated_voters = []
        stations_no = len(PollingStation.objects.filter(center=center))

        for timeslot in timeslots:
            total_service_time = Voter.objects.filter(timeslot=timeslot, center=center).aggregate(total_time=Sum('service_time'))['total_time'] or 0

            while total_service_time < 15 * stations_no and voters:
                voter = voters.pop(0)
                service_time = voter.service_time

                if total_service_time + service_time <= 15 * stations_no:
                    voter.timeslot = timeslot
                    voter.save()
                    total_service_time += service_time
                    allocated_voters.append(voter)

        return allocated_voters



class QueueDetailView(APIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            cid = request.data['cid']
            c = PollingCenter.objects.get(id=cid)

            try:
                q = Queue.objects.filter(station__center=c)
                if not q:
                    return Response({'message': f'No queue found for center: {c.name}'})
                
                serializer = QueueSerializer(q, many=True)
                return Response(serializer.data)

            except ObjectDoesNotExist:
                return Response({'error': f'Queue not found for center: {c.name}'}, status=404)

        except KeyError:
            return Response({'error': 'Invalid request. Missing "cid" parameter.'}, status=400)

        except ObjectDoesNotExist:
            return Response({'error': 'Center not found.'}, status=404)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)


class CenterDetailView(APIView):
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            cid = request.GET.get('cid')

            if not cid:
                return Response({'error': 'Invalid request. Missing "cid" parameter.'}, status=400)

            c = PollingCenter.objects.get(id=cid)
            s = Voter.objects.filter(center=c).order_by('timeslot__start')  # Sort by timeslot.start

            if s.exists():
                serializer = VoterSerializer(s, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': f'No voters found for center: {c.name}'}, status=404)
        
        except PollingCenter.DoesNotExist:
            return Response({'error': 'Center not found!'}, status=404)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)



class KimsStationsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = PollingStationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cid = request.data.get('cid')

        if not cid:
            return Response({'error': 'Invalid request. Missing "cid" parameter.'}, status=400)

        try:
            c = PollingCenter.objects.get(id=cid)
            s = PollingStation.objects.filter(center=c)

            if s.exists():
                serializer = PollingStationSerializer(s, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': f'No stations found for center: {c.name}'}, status=404)
        
        except PollingCenter.DoesNotExist:
            return Response({'error': 'Center not found!'}, status=404)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)


class KimsView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sid = request.data.get('sid')

        if not sid:
            return Response({'error': 'Invalid request. Missing "sid" parameter.'}, status=400)

        try:
            queue = self.get_queue_by_station_id(sid)
            ticket = self.get_next_ticket(queue, sid)

            if not ticket:
                return Response({'error': f'Wrong station. Please proceed to {ticket.station.name} {ticket.station.id}'}, status=404)

            if not self.can_vote(ticket):
                return Response({'error': 'Already voted!'}, status=404)

            self.update_queue_after_voting(queue, ticket)
            re_render_queue(queue)
            self.cast_vote(ticket)

            return Response({'success': f'Ticket {ticket.id} {ticket.voter.profile.first_name} {ticket.voter.profile.last_name} - {ticket.voter.profile.id_number} has cast their vote!'}, status=200)

        except Queue.DoesNotExist:
            return Response({'error': 'Queue not found!'}, status=404)

        except PollingStation.DoesNotExist:
            return Response({'error': 'Polling station not found!'}, status=404)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    def get_queue_by_station_id(self, sid):
        return Queue.objects.get(station__id=int(sid))

    def get_next_ticket(self, queue, sid):
        return queue.tickets.order_by('queue_number').first()

    def can_vote(self, ticket):
        return ticket.active

    def update_queue_after_voting(self, queue, ticket):
        queue.waiting_time -= ticket.voter.service_time
        queue.waiting_time = max(queue.waiting_time, 0.00)
        queue.current_voter_st = ticket.voter.service_time
        ticket.delete()
        queue.save()

    def cast_vote(self, ticket):
        voter = ticket.voter
        # voter.voted = True
        ticket.active = False
        Vote.objects.create(voter=voter, station=ticket.station)
        # voter.save()

        

class QueueRegistrationView(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        vid = request.data.get('id')
        cid = request.data.get('cid')
        sp = request.data.get('special')

        if not vid or not cid:
            return Response({'error': 'Invalid request. Missing "id" or "cid" parameter.'}, status=400)

        try:
            voter = Voter.objects.get(profile__id_number=vid)

            if voter.center.id != int(cid):
                return Response({'error': f'Voter not found in this center! Proceed to {voter.center.name}'}, status=404)

            if Ticket.objects.filter(voter=voter).exists():
                t = Ticket.objects.get(voter=voter)
                return Response({'error': f'Voter already has a ticket - number {t.id}'}, status=404)
            elif Vote.objects.filter(voter=voter).exists():
                return Response({'error': f'Voter already has voted!'}, status=404)
            queue = self.get_next_available_queue(voter.center, sp)
            if queue is None:
                return Response({'error': 'No available queues found.'}, status=404)

            ticket_type = self.get_ticket_type(voter, sp)
            total_service_time = self.calculate_total_service_time(queue)

            ticket = self.create_ticket(voter, queue.station, total_service_time, ticket_type)

            self.add_ticket_to_queue(queue, ticket)
            re_render_queue(queue)

            voter.ticket = ticket
            voter.save()

            return Response({'success': f'Ticket {voter.ticket.id} for {voter.profile.first_name} {voter.profile.last_name} generated successfully'}, status=200)

        except Voter.DoesNotExist:
            return Response({'error': 'Voter not found! Ensure you are a registered voter!'}, status=404)

        except PollingCenter.DoesNotExist:
            return Response({'error': 'Center not found!'}, status=404)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    def get_next_available_queue(self, center, special):
        stations = PollingStation.objects.filter(center=center)
        queues = Queue.objects.filter(station__in=stations)
        queues = queues.annotate(total_time=Sum('tickets__voter__service_time')).order_by('total_time')

        return queues.first() if queues.exists() else None

    def get_ticket_type(self, voter, special):
        current_time = datetime.datetime.now().time()
        if special:
            return 'S'
        elif voter.timeslot is not None and (voter.timeslot.start <= current_time <= voter.timeslot.stop):
            return 'A'
        else:
            return 'B'

    def calculate_total_service_time(self, queue):
        return Decimal(queue.tickets.aggregate(total_time=Sum('voter__service_time'))['total_time'] or 0)

    def create_ticket(self, voter, station, total_service_time, ticket_type):
        ticket = Ticket.objects.create(
            voter=voter,
            station=station,
            waiting_time=total_service_time,
            type=ticket_type,
            queue_number=1,
        )
        return ticket

    def add_ticket_to_queue(self, queue, ticket):
        queue.tickets.add(ticket)


class QueueBooking(APIView):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tid = request.data.get('timeslot')
        vid = request.data.get('id')

        if not tid or not vid:
            return Response({'error': 'Invalid request. Missing "timeslot" or "id" parameter.'}, status=400)

        try:
            timeslot = TimeSlot.objects.get(id=tid)
            voter = Voter.objects.get(id=vid)
            self.book_timeslot(voter, timeslot)
            return Response({"success": f"Booking for {timeslot} successful"})

        except TimeSlot.DoesNotExist:
            return Response({'error': 'Timeslot not found!'}, status=404)

        except Voter.DoesNotExist:
            return Response({'error': 'Voter not found!'}, status=404)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    def book_timeslot(self, voter, timeslot):
        stations_no = len(PollingStation.objects.filter(center=voter.center))

        total_service_time = self.calculate_total_service_time(voter, timeslot)
        if total_service_time + voter.service_time > 15 * stations_no:
            raise Exception("Timeslot already full!")

        voter.timeslot = timeslot
        voter.save()

    def calculate_total_service_time(self, voter, timeslot):
        total_service_time = Voter.objects.filter(timeslot=timeslot, center=voter.center).aggregate(total_time=Sum('service_time'))['total_time']
        return total_service_time or 0.0

        

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
                    return Response({'token': token.key, 'account_type': 'user', 'voter_id': voter.id, 'center_id': voter.center.id})
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
    queryset = PollingCenter.objects.all()
    serializer_class = PollingCenterSerializer


class PollingStationList(generics.ListCreateAPIView):
    queryset = PollingStation.objects.all()[:50]
    serializer_class = PollingStationSerializer


class PollingStationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PollingStation.objects.all()
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
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        vid = self.request.GET.get('id')
        voter = Voter.objects.get(id=vid)
        stations_no = len(PollingStation.objects.filter(center=voter.center))
        timeslots = TimeSlot.objects.all()

        # Check if each timeslot is full and set the 'full' flag
        for timeslot in timeslots:
            total_service_time = Voter.objects.filter(timeslot=timeslot, center=voter.center).aggregate(total_time=Sum('service_time'))['total_time']
            print(stations_no, timeslot,total_service_time)
            if total_service_time and total_service_time >= (15 * int(stations_no)) - 2:
                timeslot.full = True
            else:
                timeslot.full = False

        return timeslots



class TimeSlotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimeSlot.objects.all()[:50]
    serializer_class = TimeSlotSerializer


class VoteList(generics.ListCreateAPIView):
    queryset = Vote.objects.all()[:50]
    serializer_class = VoteSerializer


class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()[:50]
    serializer_class = VoteSerializer
