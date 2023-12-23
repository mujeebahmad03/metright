from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    user_type_data = ((1,"HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=100)


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
    link = models.TextField()
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
    profile_pic = models.FileField(upload_to="media/student_pic")
    address = models.TextField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


# Model of the creation of attendance by the admin of the app
class Attendance(models.Model):
    id  = models.AutoField(primary_key=True)
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
            Student.objects.create(admin=instance, course_id = Course.objects.get(id=1),level= Level.objects.get(id=1), address= "", profile_pic = "", gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()

