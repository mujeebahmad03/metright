from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.http import  HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import  messages
from .models import CustomUser, Staff, Student, Course, Subjects

def AdminHome(request):
    return render(request, "admin/home.html")

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
        try:
            user = CustomUser.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            user_type = 2
            )
            user.staff.address = address
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
        'staffs':staffs
    }
    return render(request, "admin/manageStaff.html", context)


# For updating the information of the staffs
def updateStaff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    context = {
        'staff': staff
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
        staff_id = request.POST.get('staff_id')
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            staff_model = Staff.objects.get(id=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully!")
            return HttpResponseRedirect("/updateStaff/" +staff_id)
        except:
            messages.error(request, "Error Updating Staff Info..!")
            return HttpResponseRedirect("/updateStaff/" + staff_id )


# Function for displaying the page for adding new student
def addStudent(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
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
        gender = request.POST.get('gender')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        try:
            user = CustomUser.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            user_type = 3
            )
            course_obj = Course.objects.get(id=course_id)
            user.student.course_id = course_obj
            user.student.address = address
            user.student.gender = gender
            user.student.session_start = session_start
            user.student.session_end = session_end
            user.student.profile_pic = ""
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
        'students': students
    }
    return render(request, "admin/manageStudent.html", context)


# For updating the information of the Students
def updateStudent(request, student_id):
    student = Student.objects.get(admin=student_id)
    course = Course.objects.all()
    context = {
        'student':student, 
        'courses':course
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
        address = request.POST.get('address')
        course_id = request.POST.get('course')
        gender = request.POST.get('gender')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        student_id = request.POST.get('student_id')
        try:
            user = CustomUser.objects.get(id=student_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            student_model = Student.objects.get(admin=student_id)
            student_model.address = address
            student_model.gender = gender
            student_model.session_start = session_start
            student_model.session_end = session_end

            course_model = Course.objects.get(id=course_id)
            student_model.course_id = course_model
            student_model.save()

            messages.success(request, "Student Updated Successfully!")
            return HttpResponseRedirect("/updateStudent/" + student_id)
        except:
            messages.error(request, "Error Adding Student Info..!")
            return HttpResponseRedirect("/updateStudent/" + student_id )



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
        'courses':courses
    }
    return render(request, "admin/manageCourse.html", context)


# For updating the information of the Courses
def updateCourse(request):
    return render(request, "admin/updateCourse.html")


# Function for the adding of new subjects in a particular Subject
def addSubject(request):
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type= 2)
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
            subject = Subjects(subject=subject_name, course_id=course, staff_id=staff)
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
        'subjects':subjects
    }
    return render(request, "admin/manageSubject.html", context)


# For updating the information of the Subjects
def updateSubject(request):
    return render(request, "admin/updateSubject.html")

