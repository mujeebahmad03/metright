"""metright URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from metright import  settings
from django.conf.urls.static import  static
from metapp import views, AdminView, StaffView, StudentView

urlpatterns = [
    path('checkEmail', AdminView.checkEmail, name='CheckEmail'),
    path('checkUsername', AdminView.checkUsername, name='CheckUsername'),
    path('adminHome/', AdminView.AdminHome, name="AdminHomePage"),
    path('addStaff/', AdminView.addStaff, name="AddStaff"),
    path('addStaffSave/', AdminView.addStaffSave, name="AddStaffSave"),
    path('manageStaff/', AdminView.manageStaff, name="ManageStaff"),
    path('updateStaff/<str:staff_id>/', AdminView.updateStaff, name="UpdateStaff"),
    path('editStaffSave/', AdminView.editStaffSave, name="EditStaffSave"),
    path('addStudent/', AdminView.addStudent, name="AddStudent"),
    path('addStudentSave/', AdminView.addStudentSave, name="AddStudentSave"),
    path('manageStudent/', AdminView.manageStudent, name="ManageStudent"),
    path('updateStudent/<str:student_id>/', AdminView.updateStudent, name="UpdateStudent"),
    path('editStudentSave/', AdminView.editStudentSave, name="EditStudentSave"),
    path('addCourse/', AdminView.addCourse, name="AddCourse"),
    path('addCourseSave/', AdminView.addCourseSave, name="AddCourseSave"),
    path('manageCourse/', AdminView.manageCourse, name="ManageCourse"),
    path('updateCourse/<str:course_id>/', AdminView.updateCourse, name="UpdateCourse"),
    path('editCourseSave/', AdminView.editCourseSave, name="EditCourseSave"),
    path('addSubject/', AdminView.addSubject, name="AddSubject"),
    path('addSubjectSave/', AdminView.addSubjectSave, name="AddSubjectSave"),
    path('manageSubject/', AdminView.manageSubject, name="ManageSubject"),
    path('updateSubject/<str:subject_id>/', AdminView.updateSubject, name="UpdateSubject"),
    path('editSubjectSave/', AdminView.editSubjectSave, name="EditSubjectSave"),
    path('addLevel/', AdminView.addLevel, name="AddLevel"),
    path('addLevelSave/', AdminView.addLevelSave, name="AddLevelSave"),
    path('staffFeedback/', AdminView.staffFeedback, name="StaffFeedback"),
    path('studentFeedback/', AdminView.studentFeedback, name="StudentFeedback"),
    path('studentFeedbackReply/', AdminView.studentFeedbackReply, name="StudentFeedbackReply"),
    path('staffFeedbackReply/', AdminView.staffFeedbackReply, name="StaffFeedbackReply"),
    path('staffLeave/', AdminView.staffLeave, name="StaffLeave"),
    path('staffLeaveApprove/<str:leave_id>/', AdminView.staffLeaveApprove, name="StaffLeaveApprove"),
    path('staffLeaveDisapprove/<str:leave_id>/', AdminView.staffLeaveDisapprove, name="StaffLeaveDisapprove"),
    path('studentLeave/', AdminView.studentLeave, name="StudentLeave"),
    path('studentLeaveApprove/<str:leave_id>/', AdminView.studentLeaveApprove, name="StudentLeaveApprove"),
    path('studentLeaveDisapprove/<str:leave_id>/', AdminView.studentLeaveDisapprove, name="StudentLeaveDisapprove"),

    # url patterns for the staff
    path('staffHome/', StaffView.home, name="StaffHomePage"),
    path('attendanceStudent/', StaffView.studentAttendance, name="AttendanceStudent"),
    path('getStudents/', StaffView.getStudents, name="GetStudents"),
    path('saveAttendanceData/', StaffView.saveAttendanceData, name="SaveAttendanceData"),
    path('manageAttendance/', StaffView.manageAttendance, name="ManageAttendance"),
    path('getAttendance/', StaffView.getAttendance, name="GetAttendance"),
    path('getStudentAttendance/', StaffView.getStudentAttendance, name="GetStudentAttendance"),
    path('saveUpdateAttendance/', StaffView.saveUpdateAttendance, name="saveUpdateAttendance"),
    path('leaveApply/', StaffView.leaveApply, name="LeaveApply"),
    path('leaveApplySave/', StaffView.leaveApplySave, name="LeaveApplySave"),
    path('feedbackMessage/', StaffView.feedbackMessage, name="FeedbackMessage"),
    path('feedbackSave/', StaffView.feedbackSave, name="FeedbackSave"),


    # url patterns for the student
    path('studentHome/', StudentView.home, name="StudentHomePage"),
    path('viewAttendance/', StudentView.viewAttendance, name="ViewAttendancePage"),
    path('viewAttendanceData/', StudentView.viewAttendanceData, name="ViewAttendanceData"),
    path('leaveApplyStudent/', StudentView.leaveApplyStudent, name="LeaveApplyStudent"),
    path('leaveApplySaveStudent/', StudentView.leaveApplySaveStudent, name="LeaveApplySaveStudent"),
    path('feedbackMessageStudent/', StudentView.feedbackMessageStudent, name="FeedbackMessageStudent"),
    path('feedbackSaveStudent/', StudentView.feedbackSaveStudent, name="FeedbackSaveStudent"),


    path('login/', views.loginPage, name='login'),
    path('dologin/', views.doLogin, name='DoLogin'),
    path('profile/', views.profilePage, name='ProfilePage'),
    path('logout/', views.loginPage, name='Logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

