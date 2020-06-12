from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.http import  HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
from django.contrib import  messages
from .models import (
    CustomUser, Staff, Student,
    Course, Subjects, Level, 
    Attendance, AttendanceReport,
    LeaveReportStaff, FeedBackStaff
    )
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core import  serializers
import json

def home(request):
    return render(request, 'staff/home.html')

# Taking the students attendance information views
def studentAttendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    levels = Level.objects.all()
    context = {
        'subjects':subjects,
        'levels':levels
    }
    return render(request, "staff/studentAttendance.html", context)

# creating the function to get the students according to the subjects
@csrf_exempt
def getStudents(request):
    subject_id = request.POST.get('subject')
    level = request.POST.get('level')

    subject = Subjects.objects.get(id=subject_id)
    level_model = Level.objects.get(id=level)
    students = Student.objects.filter(course_id=subject.course_id, level=level)
    student_data = serializers.serialize("python",students)
    # selection of information from the students database
    list_data = []
    for student in students:
        data_select = {"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name,}
        list_data.append(data_select)
    return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)


@csrf_exempt
# function for saving the attendance data in the ajax function
def saveAttendanceData(request):
    student_ids = request.POST.get('student_ids')
    subject_id = request.POST.get('subject')
    attendance_date = request.POST.get('attendance_date')
    level_id = request.POST.get('level')

    print(student_ids)
    subject_model = Subjects.objects.get(id=subject_id)
    level = Level.objects.get(id=level_id)
    json_student = json.loads(student_ids)

    try:
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, level=level)
        attendance.save()

        for stud in json_student:
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


# manage student attenadance views
def manageAttendance(request):
    subject = Subjects.objects.filter(staff_id=request.user.id)
    level = Level.objects.all()
    attendance = Attendance.objects.all()
    context = {
        'subjects': subject,
        'levels': level,
        'attendances': attendance
    }
    return render(request, "staff/manageAttendance.html", context)


# function for fetching the attendance data from the database
@csrf_exempt
def getAttendance(request):
    subject = request.POST.get('subject')
    level_id = request.POST.get('level')
    subject_obj = Subjects.objects.get(id=subject)
    level_obj = Level.objects.get(id=level_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, level=level_obj)
    attendance_obj=[]
    for event in attendance:
        data= {"id":event.id, "attendance_date":str(event.attendance_date), "level":event.level.id}
        attendance_obj.append(data)
    
    return JsonResponse(json.dumps(attendance_obj), safe=False)


# for fetching the attendance data of each students in the database
@csrf_exempt
def getStudentAttendance(request):
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []
    for student in attendance_data:
        data_select = {"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_select)
    return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)


@csrf_exempt
def saveUpdateAttendance(request):
    student_ids = request.POST.get('student_ids')
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    print(student_ids)
    json_student = json.loads(student_ids)

    try:

        for stud in json_student:
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


# Leave apply module
def leaveApply(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        'leave_data': leave_data
    }
    return render(request, "staff/leaveApply.html", context)


def leaveApplySave(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("LeaveApply"))
    else:
        leave_date = request.POST.get('leave_date')
        reason = request.POST.get('reason')
        
        staff_id = Staff.objects.get(admin=request.user.id)

        try:
            leave_report = LeaveReportStaff(staff_id=staff_id, leave_date=leave_date, leave_message=reason, leave_status=0)
            leave_report.save()

            messages.success(request, "Leave Application Submitted")
            return HttpResponseRedirect(reverse("LeaveApply"))

        except:
            messages.error(request, "Error Submitting Leave Application")
            return HttpResponseRedirect(reverse("LeaveApply"))


# Message Feedback Module
def feedbackMessage(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    context = {
        'feedback_data': feedback_data
    }
    return render(request, "staff/feedback.html", context)


# function for the saving of the feedback 
def feedbackSave(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("FeedbackMessage"))
    else:
        feedback_message = request.POST.get("feedback_message")
        staff_obj = Staff.objects.get(admin=request.user.id)

        try:
            feedback = FeedBackStaff(staff_id=staff_obj, feedback=feedback_message, feedback_reply="")
            feedback.save()

            messages.success(request, "Feedback Submitted")
            return HttpResponseRedirect(reverse("FeedbackMessage"))

        except:
            messages.error(request, "Error Submitting Feedback")
            return HttpResponseRedirect(reverse("FeedbackMessage"))