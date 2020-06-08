from django.shortcuts import render, HttpResponse, redirect
from metapp.EmailBackEnd import EmailBackEnd
from django.http import  HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import  messages
from .models import CustomUser, Staff, Student, Course, Subjects
from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, 'student/home.html')