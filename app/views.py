from django.shortcuts import render
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Participants, Student, StudentParticipant, Volunteer
from .forms import StudentSignupForm
from .models import Event, Organizer, College,EventParticipant,ParticipantHostel
from .models import administrator
from .forms import AdminSignupForm
from .models import Winner
from .forms import ParticipantSignupForm
from .forms import OrganizerSignupForm
from .forms import LoginForm
from .forms import RegistrationForm,StudentRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from .models import Accommodation
logger = logging.getLogger(__name__)


def events_page(request):
    # Query events from the database or create dummy data
    events = Event.objects.all()  # Query all events, you may need to adjust this query as per your model structure
    return render(request, 'events.html', {'events': events})



def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Search for the user in Student table
            user = authenticate(request,username=username,password=password)
            admin_user = administrator.objects.filter(username=username, password=password).first()
            if admin_user is not None:
                login(request, user)
                return redirect('admin_dashboard')    
            student_user = Student.objects.filter(username=username, password=password).first()
            if student_user is not None:
                login(request, user)
                return redirect('student_dashboard')  # Redirect to student dashboard
                
            # Search for the user in Participants table
            participant_user = Participants.objects.filter(username=username, password=password).first()
            if participant_user is not None:
                login(request, user)
                return redirect('participant_dashboard')  # Redirect to participant dashboard
                
            # Search for the user in Organizer table
            organizer_user = Organizer.objects.filter(username=username, password=password).first()
            if organizer_user is not None:
                login(request, user)
                return redirect('organizer_dashboard')  # Redirect to organizer dashboard
                
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'form': form, 'error': error_message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
    
    
def signup_redirect(request, signup_option):
    if signup_option == 'student':
        return redirect('signup_student')
    elif signup_option == 'participant':
        return redirect('signup_participant')
    elif signup_option == 'organizer':
        return redirect('signup_organizer')
    elif signup_option == 'Admin':
        return redirect('signup_admin')
    else:
        return redirect('login')  # Redirect to login page if option is invalid

        
def signup_student(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            roll_number = form.cleaned_data['roll_number']
            name = form.cleaned_data['name']
            department = form.cleaned_data['department']
            
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Create a new student profile
            student = Student.objects.create(Roll=roll_number, Name=name, department=department, username=username, password=password)
            student.save()
            if administrator.objects.filter(username=request.user.username).exists():
                # Redirect logged-in admin to admin dashboard after signup
                 return redirect('admin_dashboard')
            else:
                # Redirect organizer to a different page after signup
                return redirect('login') 
            # Redirect to login page after signup
    else:
        form = StudentSignupForm()
    return render(request, 'signup_student.html', {'form': form})


def signup_participant(request):
    if request.method == 'POST':
        form = ParticipantSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            college_id = form.cleaned_data['college'].CID  # Get the selected college's ID
            college_instance = College.objects.get(CID=college_id)  # Retrieve the College instance

            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Create a new participant profile
            participant = Participants.objects.create(Name=name, CID=college_instance, username=username, password=password)
            participant.save()
            if administrator.objects.filter(username=request.user.username).exists():
                # Redirect logged-in admin to admin dashboard after signup
                 return redirect('admin_dashboard')
            else:
                # Redirect organizer to a different page after signup
                return redirect('login') 
               # Redirect to login page after signup
    else:
        form = ParticipantSignupForm()
    return render(request, 'signup_participant.html', {'form': form})
    
def signup_organizer(request):
    if request.method == 'POST':
        form = OrganizerSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            event_id = form.cleaned_data['event'].EID
            event_instance = Event.objects.get(EID=event_id)  # Retrieve the College instance

            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Create a new organizer profile
            organizer = Organizer.objects.create(name=name, event_id=event_instance, username=username, password=password)
            organizer.save()
            if administrator.objects.filter(username=request.user.username).exists():
                # Redirect logged-in admin to admin dashboard after signup
                 return redirect('admin_dashboard')
            else:
                # Redirect organizer to a different page after signup
                return redirect('login') 
              # Redirect to login page after signup
    else:
        form = OrganizerSignupForm()
    return render(request, 'signup_organizer.html', {'form': form})

def signup_Admin(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            #event_id = form.cleaned_data['event'].EID
            #event_instance = Event.objects.get(EID=event_id)  # Retrieve the College instance

            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Create a new organizer profile
            admin = administrator.objects.create(username=username, password=password,a_name = name)
            admin.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = OrganizerSignupForm()
    return render(request, 'signup_admin.html', {'form': form})
    

@login_required
def student_dashboard(request):
    events = Event.objects.all()
    student = Student.objects.get(username=request.user)
    winners = Winner.objects.select_related('event', 'student', 'participant').order_by('event', 'position')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            event = Event.objects.get(EID=event_id)
            
            # Check if the event already has winners
            if not Winner.objects.filter(event=event).exists():
                # Check if the student is registering as a participant or a volunteer
                registration_type = form.cleaned_data['registration_type']
                if registration_type == 'participant':
                    # Check if student is already registered as a volunteer for this event
                    if Volunteer.objects.filter(Roll=student, EID=event).exists():
                        messages.warning(request, 'You are already registered as a volunteer for this event.')
                    else:
                        if not StudentParticipant.objects.filter(roll_number=student, event_id=event).exists():
                            StudentParticipant.objects.create(roll_number=student, event_id=event)
                            messages.success(request, 'Registered as participant successfully!')
                        else:
                            messages.warning(request, 'You are already registered as participant for this event.')
                elif registration_type == 'volunteer':
                    # Check if student is already registered as a participant for this event
                    if StudentParticipant.objects.filter(roll_number=student, event_id=event).exists():
                        messages.warning(request, 'You are already registered as participant for this event.')
                    else:
                        if not Volunteer.objects.filter(Roll=student, EID=event).exists():
                            Volunteer.objects.create(Roll=student, EID=event)
                            messages.success(request, 'Registered as volunteer successfully!')
                        else:
                            messages.warning(request, 'You are already registered as volunteer for this event.')
            else:
                messages.warning(request, 'This event already has winners, registration closed.')
            
            return redirect('student_dashboard')  # Redirect to refresh the page
    else:
        form = StudentRegistrationForm()
    
    winners = {}
    for event in events:
        event_winners = Winner.objects.filter(event=event)
        winners[event] = event_winners
    
    return render(request, 'student_dashboard.html', {'events': events, 'winners': winners, 'form': form})
@login_required
def participant_dashboard(request):
    logger.info(f"Username: {request.user.username}")
    logger.info(f"Username: {request.user.password}")
    
    hostels = Accommodation.objects.all()
    events = Event.objects.all()
    participant = Participants.objects.get(username=request.user)
    participant_id = participant.PID
    winners = Winner.objects.select_related('event', 'student', 'participant').order_by('event', 'position')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            event_id = form.cleaned_data['event_id']
            event_instance = Event.objects.get(EID=event_id)
            
            # Check if the event already has winners
            if not Winner.objects.filter(event=event_instance).exists():
                # Check if the participant is already registered for the event
                if not EventParticipant.objects.filter(EID=event_instance, PID=participant).exists():
                    EventParticipant.objects.create(EID=event_instance, PID=participant)
                    messages.success(request, 'Registered successfully!')
                else:
                    messages.warning(request, 'You are already registered for this event.')
            else:
                messages.warning(request, 'This event already has winners, registration closed.')
            
            return redirect('participant_dashboard')  # Redirect to refresh the page
    else:
        form = RegistrationForm()
    
    winners = {}
    for event in events:
        event_winners = Winner.objects.filter(event=event)
        winners[event] = event_winners
    
    return render(request, 'participant_dashboard.html', {'events': events,'hostels': hostels,'winners': winners,'form': form})

@login_required  
def organizer_dashboard(request):
    events = Event.objects.all()
    event_details = []

    for event in events:
        event_participants = EventParticipant.objects.filter(EID=event)
        student_participants = StudentParticipant.objects.filter(event_id=event)
        volunteers = Volunteer.objects.filter(EID=event)
        winners = Winner.objects.select_related('event', 'student', 'participant').order_by('event', 'position')
        event_detail = {
            'event': event,
            'event_participants': event_participants,
            'student_participants': student_participants,
            'volunteers': volunteers
        }

        event_details.append(event_detail)
    winners = {}
    for event in events:
        event_winners = Winner.objects.filter(event=event)
        winners[event] = event_winners    
    return render(request, 'organizer_dashboard.html', {'event_details': event_details,'winners':winners})
    
def admin_dashboard(request):
    # Retrieve all students, participants, and organizers
    students = Student.objects.all()
    participants = Participants.objects.all()
    organizers = Organizer.objects.all()

   

    return render(request, 'admin_dashboard.html', {'students': students, 'participants': participants, 'organizers': organizers})
   
   


 
def register_hostel(request):
    if request.method == 'POST':
        hostel_id = request.POST.get('hostel_id')
        hostel = Accommodation.objects.get(pk=hostel_id)
        participant = Participants.objects.get(username=request.user)
        # Check if participant has already booked a room
        if ParticipantHostel.objects.filter(participant=participant).exists():
            messages.warning(request, 'You have already booked a room.')
        elif hostel.rooms_available > 0:
            hostel.rooms_available -= 1
            hostel.save()
            # Create ParticipantHostel object
            ParticipantHostel.objects.create(participant=participant, hostel=hostel)
             # Remove hostel if no rooms available
    return redirect('participant_dashboard')

   
   
def delete_student(request, student_id):
    student = Student.objects.get(Roll=student_id)
    
    user = User.objects.get(username=student.username)
    user.delete()
    student.delete()
    return redirect('admin_dashboard')

def delete_organizer(request, organizer_id):
    organizer = Organizer.objects.get(org_id=organizer_id)
    user = User.objects.get(username=organizer.username)
    user.delete()
    organizer.delete()
    return redirect('admin_dashboard')

def delete_participant(request, participant_id):
    participant = Participants.objects.get(PID=participant_id)
    participant_hostel = ParticipantHostel.objects.filter(participant=participant)
    user = User.objects.get(username=participant.username)
    user.delete()
    if participant_hostel.exists():
        hostel = participant_hostel.first().hostel
        hostel.rooms_available += 1
        hostel.save()
    participant.delete()
    
   
    return redirect('admin_dashboard')
# Create your views here.
