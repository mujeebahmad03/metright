from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import (
    CustomUser, Staff, Student,
    Course, Subjects, Level,
    Attendance, AttendanceReport,
    LeaveReportStaff, FeedBackStaff,
    Reports, Assignments, AssignmentSubmission, Notes
)
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


# function for checking the email that already exists
@csrf_exempt
def checkEmailStaff(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# function for checking the username that already exists
@csrf_exempt
def checkUsernameStaff(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def home(request):
    staff_name = request.user.first_name + " " + request.user.last_name
    students = Student.objects.filter(staff=staff_name)
    students_2nd_course = Student.objects.filter(staff2=staff_name)
    students_3rd_course = Student.objects.filter(staff3=staff_name)
    # print(students_3rd_course)
    for student in students:
        print(student.admin.first_name + " " + student.admin.last_name)
    staff_count = students.count() + students_2nd_course.count() + \
        students_3rd_course.count()
    reports = Reports.objects.filter(staff=staff_name)
    assignments = Assignments.objects.filter(staff=staff_name)
    staff_name = request.user.first_name + " " + request.user.last_name
    staff_profile = Staff.objects.get(admin=request.user)
    link = staff_profile.link

    assignmentSubmissions = AssignmentSubmission.objects.filter(
        staff=staff_name)

    #print(link)
    assignmentSubmissions = AssignmentSubmission.objects.filter(
        staff=staff_name)

    context = {
        "student": students,
        "students_2nd_course": students_2nd_course,
        "students_3rd_course": students_3rd_course,
        "category_students": {
            "First Course": students,
            "Second Course": students_2nd_course,
            "Third Course": students_3rd_course,
        },
        'staff_name': staff_name,
        'staff_count': staff_count,
        'reports': reports,
        'assignmentsubmit': assignmentSubmissions,
        'assignments': assignments,
        'link': link,
    }
    return render(request, 'staff/home.html', context)

# upload student assignement


def uploadAssignment(request):
    staff_name = request.user.first_name + " " + request.user.last_name
    students = Student.objects.filter(staff=staff_name)
    students2 = Student.objects.filter(staff2=staff_name)
    students3 = Student.objects.filter(staff3=staff_name)

    context = {
        "student": students,
        "student2": students2,
        "student3": students3,
        'staff_name': staff_name,
    }

    return render(request, 'staff/uploadAssignment.html', context)


def uploadReport(request):
    staff_name = request.user.first_name + " " + request.user.last_name
    students = Student.objects.filter(staff=staff_name)
    students2 = Student.objects.filter(staff2=staff_name)
    students3 = Student.objects.filter(staff3=staff_name)

    context = {
        "student": students,
        "student2": students2,
        "student3": students3,
        'staff_name': staff_name,
    }

    return render(request, 'staff/uploadReport.html', context)

# save report


def uploadReportSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_name = request.POST.get('staff_name')
        student = request.POST.get('student')
        report = request.POST.get('image')
    
        try:
            if 'image' in request.FILES:
                profile_pic = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
                print(profile_pic_url)
                report_model = Reports(
                    staff=staff_name, student=student, report=profile_pic_url)
                report_model.save()
                messages.success(request, "Report Added Successfully!")
                return HttpResponseRedirect("/uploadReport")
            else:
                messages.error(request, "No file uploaded!")
                return HttpResponseRedirect("/uploadReport")
        except:
            messages.error(request, "Error Adding report Info..!")
            return HttpResponseRedirect("/uploadReport")

# save assignement


def uploadAssignmentSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_name = request.POST.get('staff_name')
        student = request.POST.get('student')
        report = request.POST.get('file')

        try:
            if 'image' in request.FILES:
                profile_pic = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
                assignment_model = Assignments(
                    staff=staff_name, student=student, assignment=profile_pic_url)
                assignment_model.save()
                messages.success(request, "Assignment Added Successfully!")
                return HttpResponseRedirect("/uploadAssignment")
            else:
                messages.error(request, "No image uploaded!")
                return HttpResponseRedirect("/uploadAssignment")
        except:
            messages.error(request, "Error Adding Assignement Info..!")
            return HttpResponseRedirect("/uploadAssignment")


def uploadNote(request):
    staff_name = request.user.first_name + " " + request.user.last_name
    students = Student.objects.filter(staff=staff_name)
    students2 = Student.objects.filter(staff2=staff_name)
    students3 = Student.objects.filter(staff3=staff_name)
    notes = Notes.objects.filter(staff=staff_name)

    context = {
        "student": students,
        "student2": students2,
        "student3": students3,
        'staff_name': staff_name,
        'notes': notes,
    }

    return render(request, 'staff/uploadNote.html', context)


def uploadNoteSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_name = request.POST.get('staff_name')
        student = request.POST.get('student')
        note = request.POST.get('file')

        try:
            if 'image' in request.FILES:
                profile_pic = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
                notes_model = Notes(
                    staff=staff_name, student=student, note=profile_pic_url)
                notes_model.save()
                messages.success(request, "Notes Added Successfully!")
                return HttpResponseRedirect("/uploadNote")
            else:
                messages.error(request, "No file uploaded!")
                return HttpResponseRedirect("/uploadNote")
        except:
            messages.error(request, "Error Adding Notes Info..!")
            return HttpResponseRedirect("/uploadNote")


# Taking the students attendance information views
def studentAttendance(request):
    # subjects = Subjects.objects.filter(staff_id=request.user.id)
    subjects = Subjects.objects.all()
    levels = Level.objects.all()
    context = {
        'subjects': subjects,
        'levels': levels
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
    student_data = serializers.serialize("python", students)
    # selection of information from the students database
    list_data = []
    for student in students:
        data_select = {"id": student.admin.id,
                       "name": student.admin.first_name+" "+student.admin.last_name, }
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
        attendance = Attendance(subject_id=subject_model,
                                attendance_date=attendance_date, level=level)
        attendance.save()

        for stud in json_student:
            student = Student.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(
                student_id=student, attendance_id=attendance, status=stud['status'])
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
    attendance = Attendance.objects.filter(
        subject_id=subject_obj, level=level_obj)
    attendance_obj = []
    for event in attendance:
        data = {"id": event.id, "attendance_date": str(
            event.attendance_date), "level": event.level.id}
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
        data_select = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name +
                       " "+student.student_id.admin.last_name, "status": student.status}
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
            attendance_report = AttendanceReport.objects.get(
                student_id=student, attendance_id=attendance)
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
            leave_report = LeaveReportStaff(
                staff_id=staff_id, leave_date=leave_date, leave_message=reason, leave_status=0)
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
            feedback = FeedBackStaff(
                staff_id=staff_obj, feedback=feedback_message, feedback_reply="")
            feedback.save()

            messages.success(request, "Message Submitted")
            return HttpResponseRedirect(reverse("FeedbackMessage"))

        except:
            messages.error(request, "Error Submitting Message")
            return HttpResponseRedirect(reverse("FeedbackMessage"))


#  profile page for the staff of the app
def userProfileStaff(request):
    user_data = CustomUser.objects.get(id=request.user.id)
    # staff = Staff.objects.get(id=request.user.id)
    context = {
        'user_data': user_data,
        # 'staff':staff
    }
    return render(request, "staff/profile.html", context)


def editProfileSaveStaff(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("UserProfileStaff"))
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        link = request.POST.get('link')
        gender = request.POST.get('gender')
        staff_id = request.POST.get('Admin_id')

        if request.FILES.get('image', False):
            profile_pic = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            # staff = Staff.objects.get(id=request.user.id)
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.username = username
            customuser.email = email
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staff.objects.get(admin=staff_id)

            if profile_pic_url != None:
                staff.profile_pic = profile_pic_url

            staff.address = address
            staff.gender = gender
            staff.link = link
            staff.profile_pic = profile_pic_url
            staff.save()

            messages.success(request, "Staff Profile Updated Successfully")
            return HttpResponseRedirect(reverse("UserProfileStaff"))
        except:
            messages.error(request, "Error Updating Staff Profile")
            return HttpResponseRedirect(reverse("UserProfileStaff"))
