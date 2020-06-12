from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.http import  HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import  messages
import datetime

from .models import ( 
    CustomUser, Staff, Student, Course, Subjects, Level, Attendance, AttendanceReport
)
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, 'student/home.html')


# module for the view of the attendance records by the student
def viewAttendance(request):
    student = Student.objects.get(admin=request.user.id)
    courses = Course.objects.get(id=student.course_id.id)
    subject = Subjects.objects.filter(course_id=courses)
    level = Level.objects.all()

    context = {
        'subjects':subject,
        'levels': level
    }
    return render(request, "student/viewAttendance.html", context)


# for fetching the student attendance data
def viewAttendanceData(request):
    subject = request.POST.get('subject')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_model = Subjects.objects.get(id=subject)
    stud_obj = Student.objects.get(admin=request.user.id)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_model)
    attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

    context = {
        'attendance_report': attendance_report
    }
    
    return render(request, "student/attendanceData.html", context)
    