from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.urls import  reverse
from django.http import  HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import  messages
import datetime

from .models import ( 
    CustomUser, Staff, Student, Course, Subjects, Level, Attendance, AttendanceReport,
    LeaveReportStudent, FeedBackStudent

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
    

# Leave apply module
def leaveApplyStudent(request):
    student_obj = Student.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        'leave_data': leave_data
    }
    return render(request, "student/leaveApplyStudent.html", context)


def leaveApplySaveStudent(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("LeaveApplyStudent"))
    else:
        leave_date = request.POST.get('leave_date')
        reason = request.POST.get('reason')
        
        student_id = Student.objects.get(admin=request.user.id)

        try:
            leave_report = LeaveReportStudent(student_id=student_id, leave_date=leave_date, leave_message=reason, leave_status=0)
            leave_report.save()

            messages.success(request, "Leave Application Submitted")
            return HttpResponseRedirect(reverse("LeaveApplyStudent"))

        except:
            messages.error(request, "Error Submitting Leave Application")
            return HttpResponseRedirect(reverse("LeaveApplyStudent"))


# Message Feedback Module
def feedbackMessageStudent(request):
    student_obj = Student.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        'feedback_data': feedback_data
    }
    return render(request, "student/feedbackStudent.html", context)


# function for the saving of the feedback 
def feedbackSaveStudent(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("FeedbackMessage"))
    else:
        feedback_message = request.POST.get("feedback_message")
        student_obj = Student.objects.get(admin=request.user.id)

        try:
            feedback = FeedBackStudent(student_id=student_obj, feedback=feedback_message, feedback_reply="")
            feedback.save()

            messages.success(request, "Feedback Submitted")
            return HttpResponseRedirect(reverse("FeedbackMessageStudent"))

        except:
            messages.error(request, "Error Submitting Feedback")
            return HttpResponseRedirect(reverse("FeedbackMessageStudent"))