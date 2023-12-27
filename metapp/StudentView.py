from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime

from .models import (
    CustomUser, Staff, Student, Course, Subjects, Level, Attendance, AttendanceReport,
    LeaveReportStudent, FeedBackStudent, Reports

)
from django.core.files.storage import FileSystemStorage


# function for checking the email that already exists
@csrf_exempt
def checkEmailStudent(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# function for checking the username that already exists
@csrf_exempt
def checkUsernameStudent(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def home(request):
    student = Student.objects.get(admin=request.user.id)
    student_name = request.user.first_name + " " + request.user.last_name
    print(student_name)
    attendance = AttendanceReport.objects.filter(student_id=student).count()
    attendance_present = AttendanceReport.objects.filter(
        student_id=student, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(
        student_id=student, status=False).count()
    course = Course.objects.get(id=student.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()
    staff = Staff.objects.all()
    reports = Reports.objects.filter(student=student_name)
    context = {
        'total_attendance': attendance,
        'present': attendance_present,
        'present': attendance_absent,
        'subjects': subjects,
        'student': student,
        'course': course,
        'staff': staff,
        'reports':reports,
    }
    return render(request, 'student/home.html', context)


# module for the view of the attendance records by the student
def viewAttendance(request):
    student = Student.objects.get(admin=request.user.id)
    courses = Course.objects.get(id=student.course_id.id)
    subject = Subjects.objects.filter(course_id=courses)
    level = Level.objects.all()

    context = {
        'subjects': subject,
        'levels': level
    }
    return render(request, "student/viewAttendance.html", context)


# for fetching the student attendance data
def viewAttendanceData(request):
    subject = request.POST.get('subject')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    start_date_parse = datetime.datetime.strptime(
        start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_model = Subjects.objects.get(id=subject)
    stud_obj = Student.objects.get(admin=request.user.id)

    attendance = Attendance.objects.filter(attendance_date__range=(
        start_date_parse, end_date_parse), subject_id=subject_model)
    attendance_report = AttendanceReport.objects.filter(
        attendance_id__in=attendance, student_id=stud_obj)

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
            leave_report = LeaveReportStudent(
                student_id=student_id, leave_date=leave_date, leave_message=reason, leave_status=0)
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
            feedback = FeedBackStudent(
                student_id=student_obj, feedback=feedback_message, feedback_reply="")
            feedback.save()

            messages.success(request, "Feedback Submitted")
            return HttpResponseRedirect(reverse("FeedbackMessageStudent"))

        except:
            messages.error(request, "Error Submitting Feedback")
            return HttpResponseRedirect(reverse("FeedbackMessageStudent"))

#  profile page for the Student of the app


def userProfileStudent(request):
    student = Student.objects.get(admin=request.user.id)
    user_data = CustomUser.objects.get(id=request.user.id)
    context = {
        'user_data': user_data,
        'student': student
    }
    return render(request, "student/profile.html", context)


def editProfileSaveStudent(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("UserProfileStudent"))
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.username = username
            customuser.email = email
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Student.objects.get(admin=customuser)
            student.address = address
            student.save()

            messages.success(request, "Student Profile Updated Successfully")
            return HttpResponseRedirect(reverse("UserProfileStudent"))
        except:
            messages.error(request, "Error Updating Student Profile")
            return HttpResponseRedirect(reverse("UserProfileStudent"))
