from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from metapp.EmailBackEnd import EmailBackEnd
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import (
    CustomUser, Staff, Student, Course, Subjects, Level,
    FeedBackStaff, FeedBackStudent,
    LeaveReportStaff, LeaveReportStudent, Attendance,
    AttendanceReport, Reports, Assignments, AssignmentSubmission,
    Reciepts, Invoice
)
from django.core.files.storage import FileSystemStorage
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def AdminHome(request):
    staff_count = Staff.objects.count()
    student_count = Student.objects.count()
    subject_count = Subjects.objects.count()
    reports = Reports.objects.all()
    assignment = Assignments.objects.all()
    assignmentsubmit = AssignmentSubmission.objects.all()
    context = {
        'staff_count': staff_count,
        'student_count': student_count,
        'subject_count': subject_count,
        "reports": reports,
        'assignments': assignment,
        'assignmentsubmit': assignmentsubmit,
    }
    return render(request, "admin/home.html", context)


def payments(request):
    students = Student.objects.all()
    invoice = Invoice.objects.all()
    receipts = Reciepts.objects.all()
    context = {
        'students': students,
        'invoices': invoice,
        'receipts': receipts}
    return render(request, "admin/payments.html", context)


def paymentsInvoice(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student = request.POST.get('student')

        try:
            if 'image' in request.FILES:
                invoice = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(invoice.name, invoice)
                invoice_url = fs.url(filename)

                invoice_model = Invoice(student=student, invoice=invoice_url)
                invoice_model.save()
                messages.success(request, "Invoice Added Successfully!")
                return HttpResponseRedirect("/payments")
            else:
                messages.error(request, "No file uploaded!")
                return HttpResponseRedirect("/payments")
        except:
            messages.error(request, "Error Adding Invoice Info..!")
            return HttpResponseRedirect("/payments")


# Function for displaying the page for adding new staff
def addStaff(request):
    return render(request, "admin/addStaff.html")

# Function for the saving of the information inputed in the add staffpage


def addStaffSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        link = request.POST.get('link')
        gender = request.POST.get('gender')
        try:
            user = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                user_type=2,
            )

            if request.FILES.get('image', False):
                profile_pic = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            user.staff.profile_pic = profile_pic_url

            user.staff.address = address
            user.staff.link = link
            user.staff.gender = gender
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return HttpResponseRedirect("/addStaff")
        except:
            messages.error(request, "Error Adding Staff Info..!")
            return HttpResponseRedirect("/addStaff")

# For managing the staffs


def manageStaff(request):
    staffs = Staff.objects.all()
    context = {
        'staffs': staffs
    }
    return render(request, "admin/manageStaff.html", context)



def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, admin__id=staff_id)

    if request.method == 'POST':
        staff.delete()
        #return redirect('manageStaff.html')  # Redirect to your staff list view after deletion
        return HttpResponseRedirect("/adminHome/")

    return render(request, '/adminHome.html')


def delete_student(request, student_id):
    student = get_object_or_404(Student, admin__id=student_id)

    if request.method == 'POST':
        student.delete()
        return HttpResponseRedirect("/adminHome/")

    return render(request, '/adminHome.html')


# For updating the information of the staffs
def updateStaff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    context = {
        'staff': staff,
        'id': staff_id
    }
    return render(request, "admin/updateStaff.html", context)

# For saving the information updated in the staff


def editStaffSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        link = request.POST.get('link')
        gender = request.POST.get('gender')
        staff_id = request.POST.get('staff_id')

        if request.FILES.get('image', False):
            profile_pic = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if password != None and password != "":
                user.set_password(password)

            user.save()

            staff_model = Staff.objects.get(admin=staff_id)
            if profile_pic_url != None:
                staff_model.profile_pic = profile_pic_url

            staff_model.address = address
            staff_model.gender = gender
            staff_model.link = link
            staff_model.profile_pic = profile_pic_url
            staff_model.save()

            messages.success(request, "Staff Updated Successfully!")
            return HttpResponseRedirect("/updateStaff/" + staff_id)
        except:
            messages.error(request, "Error Updating Staff Info..!")
            return HttpResponseRedirect("/updateStaff/" + staff_id)


# Function for displaying the page for adding new student
def addStudent(request):
    courses = Course.objects.all()
    level = Level.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'courses': courses,
        'levels': level,
        'staffs': staff
    }
    return render(request, "admin/addStudent.html", context)


# Function for saving the information passed from the addstudent page
def addStudentSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        course_id = request.POST.get('course')
        course2_id = request.POST.get('course2')
        course3_id = request.POST.get('course3')
        gender = request.POST.get('gender')
        level_id = request.POST.get('level')
        staff = request.POST.get("staff")
        staff2 = request.POST.get("staff2")
        staff3 = request.POST.get("staff3")

        try:
            user = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                user_type=3
            )
            course_obj = Course.objects.get(id=course_id)
            
            if course2_id == 0:
                pass
            else:
                course_obj2 = Course.objects.get(id=course2_id)
            
            if course3_id == 0:
                pass
            else:   
                course_obj3 = Course.objects.get(id=course3_id)
                
            user.student.course_id = course_obj
            user.student.course2_id = course_obj2
            user.student.course3_id = course_obj3
            user.student.address = address
            user.student.gender = gender
            user.student.staff = staff
            user.student.staff2 = staff2
            user.student.staff3 = staff3
            level_obj = Level.objects.get(id=level_id)
            user.student.level = level_obj

            if request.FILES.get('image', False):
                profile_pic = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            user.student.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Student Added Successfully!")
            return HttpResponseRedirect("/addStudent")
        except:
            messages.error(request, "Error Adding Student Info..!")
            return HttpResponseRedirect("/addStudent")

# For managing the students


def manageStudent(request):
    students = Student.objects.all()
    context = {
        'students': students,
    }
    return render(request, "admin/manageStudent.html", context)


# For updating the information of the Students
def updateStudent(request, student_id):
    student = Student.objects.get(admin=student_id)
    course = Course.objects.all()
    level = Level.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'student': student,
        'courses': course,
        'id': student_id,
        'levels': level,
        'staffs': staff
    }
    return render(request, "admin/updateStudent.html", context)


# For saving the information updated in the Student
def editStudentSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        course_id = request.POST.get('course')
        course2_id = request.POST.get('course2')
        course3_id = request.POST.get('course3')
        gender = request.POST.get('gender')
        level_id = request.POST.get('level')
        student_id = request.POST.get('student_id')
        staff = request.POST.get("staff")
        staff2 = request.POST.get("staff2")
        staff3 = request.POST.get("staff3")

        if request.FILES.get('image', False):
            profile_pic = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if password != None and password != "":
                user.set_password(password)

            user.save()

            student_model = Student.objects.get(admin=student_id)
            student_model.address = address
            student_model.gender = gender
            student_model.staff = staff
            student_model.staff2 = staff2
            student_model.staff3 = staff3

            if profile_pic_url != None:
                student_model.profile_pic = profile_pic_url
            course_model = Course.objects.get(id=course_id)
            course_model2 = Course.objects.get(id=course2_id)
            course_model3 = Course.objects.get(id=course3_id)
                
            student_model.course_id = course_model
            student_model.course2_id = course_model2
            student_model.course3_id = course_model3
            
            level_model = Level.objects.get(id=level_id)
            student_model.level = level_model
            student_model.save()

            messages.success(request, "Student Updated Successfully!")
            return HttpResponseRedirect("/updateStudent/" + student_id)
        except:
            messages.error(request, "Error Adding Student Info..!")
            return HttpResponseRedirect("/updateStudent/" + student_id)


# adding new Course in the app
def addCourse(request):
    return render(request, "admin/addCourse.html")


# Saving the information in the add coursepage
def addCourseSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get('coursename')
        try:
            course_model = Course(course=course)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return HttpResponseRedirect("/addCourse")
        except:
            messages.error(request, "Error Adding Course!")
            return HttpResponseRedirect("/addCourse")

# function for the management of the Course in the site


def manageCourse(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, "admin/manageCourse.html", context)


# For updating the information of the Courses
def updateCourse(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        'course': course,
        'id': course_id
    }
    return render(request, "admin/updateCourse.html", context)


def editCourseSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('coursename')
        try:
            course = Course.objects.get(id=course_id)
            course.course = course_name
            course.save()

            messages.success(request, "Course Updated Successfully!")
            return HttpResponseRedirect("/updateCourse/" + course_id)
        except:
            messages.error(request, "Error Updating Course!")
            return HttpResponseRedirect("/updateCourse/" + course_id)


# Function for the adding of new subjects in a particular Subject
def addSubject(request):
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {
        'courses': courses,
        'staffs': staffs
    }
    return render(request, "admin/addSubject.html", context)


# Saving the information in the add Subjectpage
def addSubjectSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name = request.POST.get('subjectname')
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject=subject_name,
                               course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return HttpResponseRedirect("/addSubject")
        except:
            messages.error(request, "Error Adding Subject!")
            return HttpResponseRedirect("/addSubject")


# function for the management of the Subjects in the site
def manageSubject(request):
    subjects = Subjects.objects.all()
    context = {
        'subjects': subjects
    }
    return render(request, "admin/manageSubject.html", context)


# For updating the information of the Subjects
def updateSubject(request, subject_id):
    staff = CustomUser.objects.filter(user_type=2)
    course = Course.objects.all()
    subject = Subjects.objects.get(id=subject_id)

    context = {
        'staffs': staff,
        'courses': course,
        'subject': subject,
        'id': subject_id
    }

    return render(request, "admin/updateSubject.html", context)

# Function for saving the information updated in the subjects


def editSubjectSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")

    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subjectname')
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject = subject_name
            subject.save()

            messages.success(request, "Subject Updated Successfully!")
            return HttpResponseRedirect("/updateSubject/" + subject_id)
        except:
            messages.error(request, "Error Updating Subject!")
            return HttpResponseRedirect("/updateSubject/" + subject_id)


# for addind levels in the site
def addLevel(request):
    return render(request, "admin/addLevel.html")


def addLevelSave(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        level = request.POST.get('level')
        try:
            level_model = Level(level=level)
            level_model.save()
            messages.success(request, "level Added Successfully!")
            return HttpResponseRedirect("/addLevel")
        except:
            messages.error(request, "Error Adding level!")
            return HttpResponseRedirect("/addLevel")

# for feedback reply of staff


def staffFeedback(request):
    feedback_data = FeedBackStaff.objects.all()
    context = {
        'feedback_data': feedback_data
    }
    return render(request, "admin/staffFeedback.html", context)


@csrf_exempt
# reply function for the staff feedback
def staffFeedbackReply(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')

    try:
        feedback = FeedBackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()

        return HttpResponse("True")
    except:
        return HttpResponse("False")


# for feedback reply of students
def studentFeedback(request):
    feedback_data = FeedBackStudent.objects.all()
    context = {
        'feedback_data': feedback_data
    }
    return render(request, "admin/studentFeedback.html", context)


@csrf_exempt
# reply function for the student feedback
def studentFeedbackReply(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')
    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()

        return HttpResponse("True")
    except:
        return HttpResponse("False")


# function for checking the email that already exists
@csrf_exempt
def checkEmail(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# function for checking the username that already exists
@csrf_exempt
def checkUsername(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

# staff leave views


def staffLeave(request):
    leave_data = LeaveReportStaff.objects.all()
    context = {
        'leave_data': leave_data
    }
    return render(request, "admin/staffLeave.html", context)

# function for the approval of the Staff leave


def staffLeaveApprove(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("StaffLeave"))


# function for the disapproval of the Staff leave
def staffLeaveDisapprove(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("StaffLeave"))


# student leave views
def studentLeave(request):
    leave_data = LeaveReportStudent.objects.all()
    context = {
        'leave_data': leave_data
    }
    return render(request, "admin/studentLeave.html", context)

# function for the approval of the student leave


def studentLeaveApprove(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("StudentLeave"))


# function for the disapproval of the student leave
def studentLeaveDisapprove(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("StudentLeave"))


def viewAttendance(request):
    subject = Subjects.objects.all()
    level = Level.objects.all()
    attendance = Attendance.objects.all()
    context = {
        'subjects': subject,
        'levels': level,
        'attendances': attendance
    }
    return render(request, "admin/viewAttendance.html", context)


@csrf_exempt
def getAttendanceDate(request):
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


@csrf_exempt
def getStudentAttendanceAdmin(request):
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []
    for student in attendance_data:
        data_select = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name +
                       " "+student.student_id.admin.last_name, "status": student.status}
        list_data.append(data_select)
    return JsonResponse(json.dumps(list_data), content_type='application/json', safe=False)


#  profile page for the admin of the app
def userProfile(request):
    user_data = CustomUser.objects.get(id=request.user.id)
    context = {
        'user_data': user_data
    }
    return render(request, "admin/profile.html", context)


def editProfileSave(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("UserProfile"))
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.username = username
            customuser.email = email
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            messages.success(request, "Admin Profile Updated Successfully")
            return HttpResponseRedirect(reverse("UserProfile"))
        except:
            messages.error(request, "Error Updating Admin Profile")
            return HttpResponseRedirect(reverse("UserProfile"))
