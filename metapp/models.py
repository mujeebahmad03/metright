from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.conf import settings

AWS_STORAGE_BUCKET_NAME = 'brint-media-bkt-24'

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
MEDIA_ROOT = '/media/'
MEDIA_URL =  f'https://{AWS_S3_CUSTOM_DOMAIN}{MEDIA_ROOT}'

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=100)


# Model for the admin of the site
class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Staffs models
class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    link = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.FileField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Courses in the site
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# The subjects in the school
class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=200)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# creating levels models in the app
class Level(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Model of the student in the site
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100)
    profile_pic = models.FileField()
    address = models.TextField()
    staff = models.TextField(blank=True, null=True)
    staff2 = models.TextField(blank=True, null=True)
    staff3 = models.TextField(blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='primary_course_students', blank=True, null=True)
    course2_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='secondary_course_students', blank=True, null=True)
    course3_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tertiary_course_students', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Reciepts(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    reciept = models.FileField()
    
class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    invoice = models.FileField()

# model for the reports upload by staff
class Reports(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.TextField()
    student = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    report = models.FileField()


# model for the notes upload by staff
class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.TextField()
    student = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    note = models.FileField()



# model for the assignement upload by staff
class Assignments(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.TextField()
    student = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    assignment = models.FileField()

# for students assignments submissions
class AssignmentSubmission(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.TextField()
    student = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    assignment = models.FileField()



# Model of the creation of attendance by the admin of the app
class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Model of the attendance report in the site
class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# For creation of leave by the students
class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=200)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# For creation of leave by the Staffs
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=200)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# For creation of Feedback by the admin for the students
class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# For creation of Feedback by the admin for the staff
class FeedBackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# For creation of notification for the staff
class NotificationStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# For creation of notification for the student
class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Creating django signals to automatically create profiles for the students and tje staff upon adding new
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Student.objects.create(admin=instance, course_id=Course.objects.get(
                id=1), level=Level.objects.get(id=1), address="", profile_pic="", gender="", staff="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
