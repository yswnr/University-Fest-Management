from django.db import models
from django.db import models



    
class College(models.Model):
    CID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

class Student(models.Model):
    Roll = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

class Event(models.Model):
    EID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50)
    EDate = models.DateField()
    Type = models.CharField(max_length=50)
    description = models.CharField(max_length = 1000,null = True)
    venue = models.CharField(max_length = 100,null = True)

    def __str__(self):
        return self.Name

class Participants(models.Model):
    PID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    CID = models.ForeignKey(College, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.Name

class Volunteer(models.Model):
    VID = models.AutoField(primary_key=True)
    Roll = models.ForeignKey(Student, on_delete=models.CASCADE)
    EID = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Volunteer {self.VID}"

class EventParticipant(models.Model):
    EID = models.ForeignKey(Event, on_delete=models.CASCADE)
    PID = models.ForeignKey(Participants, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('EID', 'PID'),)

    def __str__(self):
        return f"Event: {self.EID}, Participant: {self.PID}"
class StudentParticipant(models.Model):
    roll_number = models.ForeignKey(Student, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student: {self.roll_number}, Event: {self.event_id}"
class Organizer(models.Model):
    org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=100)

    def __str__(self):
        return self.admin_name
class administrator(models.Model):
    a_id = models.AutoField(primary_key=True)
    a_name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length=100)
   

    def __str__(self):
        return self.a_name
class Accommodation(models.Model):
    hostel_id = models.AutoField(primary_key=True)
    hostel_name = models.CharField(max_length=100)
    rooms_available = models.IntegerField()

    def __str__(self):
        return self.hostel_name
        
class Winner(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    position = models.IntegerField(choices=[(1, '1st'), (2, '2nd'), (3, '3rd')])
    student = models.ForeignKey('Student', null=True, blank=True, on_delete=models.CASCADE)
    participant = models.ForeignKey('Participants', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('event', 'position')  # Ensure each position is unique for each event

    def __str__(self):
        if self.student:
            return f'Event: {self.event.Name}, Position: {self.get_position_display()}, Student: {self.student.Name}'
        elif self.participant:
            return f'Event: {self.event.Name}, Position: {self.get_position_display()}, Participant: {self.participant.Name}'
        else:
            return f'Event: {self.event.Name}, Position: {self.get_position_display()}, No winner specified'
            
class ParticipantHostel(models.Model):
    participant = models.ForeignKey('Participants', on_delete=models.CASCADE)
    hostel = models.ForeignKey('Accommodation', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('participant', 'hostel')  # Ensure each participant can book only one room in one hostel

    def __str__(self):
        return f'Participant: {self.participant.Name}, Hostel: {self.hostel.hostel_name}'
    
    

# Create your models here.
# Create your models here.
# Create your models here.
