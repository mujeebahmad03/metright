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
    LeaveReportStudent, FeedBackStudent, Reports, Assignments,
    AssignmentSubmission, Reciepts, Invoice, Notes
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
    attendance = AttendanceReport.objects.filter(student_id=student).count()
    attendance_present = AttendanceReport.objects.filter(
        student_id=student, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(
        student_id=student, status=False).count()
    course = Course.objects.get(id=student.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()
    staff = Staff.objects.all()
    reports = Reports.objects.filter(student=student_name)
    assignments = Assignments.objects.filter(student=student_name)
    student_staff = request.user.student.staff
    assignmentSubmissions = AssignmentSubmission.objects.filter(student=student_name)
    
    context = {
        'total_attendance': attendance,
        'present': attendance_present,
        'present': attendance_absent,
        'subjects': subjects,
        'student': student,
        'course': course,
        'staff': staff,
        'reports': reports,
        'assignmentsubmit':assignmentSubmissions,
        'assignments': assignments,
    }
    return render(request, 'student/home.html', context)


def studentNotes(request):
    student = Student.objects.get(admin=request.user.id)
    student_name = request.user.first_name + " " + request.user.last_name
    notes = Notes.objects.filter(student=student_name)
    
    context = {
        'notes':notes,
    }
    
    return render(request, "student/notes.html", context)
    
# save assignement
def studentUploadAssignmentSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_name = request.POST.get('student_staff')
        student = request.POST.get('student_name')
        assignment = request.POST.get('file')

        try:
            if 'image' in request.FILES:
                profile_pic = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
                assignment_model = AssignmentSubmission(
                    staff=staff_name, student=student, assignment=profile_pic_url)
                assignment_model.save()
                messages.success(request, "Assignment Added Successfully!")
                return HttpResponseRedirect("/studentUploadAssignment")
            else:
                messages.error(request, "No file uploaded!")
                return HttpResponseRedirect("/studentUploadAssignment")
        except:
            messages.error(request, "Error Submitting Assignement Info..!")
            return HttpResponseRedirect("/studentUploadAssignment")

# upload student assignement
def studentUploadAssignment(request):
    #staff_name = request.user.first_name + " " + request.user.last_name
    #students = Student.objects.filter(staff=staff_name)
    student = Student.objects.get(admin=request.user.id)
    student_name = request.user.first_name + " " + request.user.last_name
    student_staff = request.user.student.staff
    assignmentSubmissions = AssignmentSubmission.objects.filter(student=student_name)
    context = {
        "student": student,
        'student_name': student_name,
        'student_staff': student_staff,
        'assignments':assignmentSubmissions,
    }

    return render(request, 'student/uploadAssignment.html', context)


# upload student payment reciept
def studentPayment(request):
    student = Student.objects.get(admin=request.user.id)
    student_name = request.user.first_name + " " + request.user.last_name
    studentInvoice = Invoice.objects.filter(student=student_name)
    studentReciept = Reciepts.objects.filter(student=student_name)
    context = {
        "student": student,
        'student_name': student_name,
        'invoices':studentInvoice,
        'reciepts':studentReciept
    }

    return render(request, 'student/payment.html', context)

# save reciept
def studentRecieptSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student = request.POST.get('student_name')
        try:
            if 'image' in request.FILES:
                receipt = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(receipt.name, receipt)
                reciept_url = fs.url(filename)
                reciept_model = Reciepts(student=student, reciept=reciept_url)
                reciept_model.save()
                messages.success(request, "Receipt Added Successfully!")
                return HttpResponseRedirect("/studentPayment")
            else:
                messages.error(request, "No file uploaded!")
                return HttpResponseRedirect("/studentPayment")
        except:
            messages.error(request, "Error Submitting Receipt Info..!")
            return HttpResponseRedirect("/studentPayment")


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
    student = Student.objects.get(admin=request.user.id)
    context = {
        'leave_data': leave_data,
        'student': student,
        
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
    student = Student.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        'feedback_data': feedback_data,
        'student':student,
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

            messages.success(request, "Message Submitted")
            return HttpResponseRedirect(reverse("FeedbackMessageStudent"))

        except:
            messages.error(request, "Error Submitting Message")
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
        gender = request.POST.get('gender')
        
        if request.FILES.get('image', False):
            profile_pic = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
            
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
            student.gender = gender
            if profile_pic_url != None:
                student.profile_pic = profile_pic_url
            student.save()

            messages.success(request, "Student Profile Updated Successfully")
            return HttpResponseRedirect(reverse("UserProfileStudent"))
        except:
            messages.error(request, "Error Updating Student Profile")
            return HttpResponseRedirect(reverse("UserProfileStudent"))
