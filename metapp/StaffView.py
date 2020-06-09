from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.http import  HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import  messages
from .models import CustomUser, Staff, Student, Course, Subjects, Level, Attendance, AttendanceReport
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