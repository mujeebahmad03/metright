from django.utils.deprecation import MiddlewareMixin
from django.http import  HttpResponseRedirect
from django.urls import  reverse

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "metapp.AdminView":
                    pass
                elif modulename == "metapp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("AdminHomePage"))
            elif user.user_type == "2":
                if modulename == "metapp.StaffView":
                    pass
                elif modulename == "metapp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("StaffHomePage"))
            elif user.user_type == "3":
                if modulename == "metapp.StudentView":
                    pass
                elif modulename == "metapp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("StudentHomePage"))
            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            if request.path == reverse('login') or request.path == reverse('DoLogin'):
                pass
            else:
                return HttpResponseRedirect(reverse('login'))
