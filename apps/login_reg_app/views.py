from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, "login_reg_app/index.html")

def registration(request):
    result = User.objects.validateReg(request)

    if result[0] == False:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
        return render(request, "login_reg_app/index.html")

    return log_user_in(request, result[1])

def quotes(request):
    if not 'user' in request.session:
        return redirect('/')
    return render(request, 'login_reg_app/quotes.html')

def login(request):
    result = User.objects.validateLogin(request)

    if result[0] == False:
        messages.add_message(request, messages.INFO, "Email/password don't match.")
        return render(request, "login_reg_app/index.html")

    return log_user_in(request, result[1])


def log_user_in(request, user):
    request.session['user'] = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return render(request, 'login_reg_app/quotes.html')

# def contribute(request):
#     if not check_logged_in(request):
#         return redirect('/')
#
#     result = Quotes.objects.contribute(request.POST, request.session['user']['id'])
#
#     if result[0] == True:
#         return redirect(request, '/quotes.html')
