from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from backend import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
# from . import send_mail




# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


@csrf_exempt
def check_login_status(request):
    user= request.user

    if request.user.is_authenticated:
        return JsonResponse({"message": f"{user.username} is logged in."})
    else:
        return JsonResponse({"message": "User is not logged in."}, status=401)


@csrf_exempt
def signup(request):
    if request.method == "POST":          
        data=json.loads(request.body) 
        username=data.get('username','') 
        fname=data.get('fname','') 
        lname=data.get('lname','')         
        email=data.get('email','')
        pass1=data.get('pass1','')
        pass2=data.get('pass2','')

        if User.objects.filter(username=username):
            return JsonResponse({
                'status':False,
                'message': 'Username already exists!!',         
            },status=400)
        
        if User.objects.filter(email=email):
          
            return JsonResponse({
                'status':False,
                'message': 'Email already registered!',         
            },status=400)
        
        if len(username)>10:
            return JsonResponse({
                'status':False,
                'message': "Username must be under 10 characters",         
            },status=400)

        if pass1 != pass2:
            return JsonResponse({
                'status':False,
                'message': "Passwords didn't match!",         
            },status=400)

        if not username.isalnum():
            return JsonResponse({
                'status':False,
                'message': "username must be Alpha-Numeric!",         
            },status=400)

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()



        subject = "Welcome to YTAnalytics -- Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to YTAnalytics!!\nThank you for visiting our website\nWe have also sent you a confirmation email, please confirm your email address in order to activate your account.\nThanking you\nYTAnalytics" 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        #Email address confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ YTAnalytics -- Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = False
        email.send()

        return JsonResponse({
                'status':True,
                'message': "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.",         
            })

    # return render(request, "authentication/signup.html")

@csrf_exempt
def signin(request):

    if request.method == "POST":
        data=json.loads(request.body)
        username =data.get('username','')
        pass1 = data.get('pass1','')
    
        user=authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            response_data = {
                'status':True,
                'message': 'Logged in successfully',
                'username': username,              
            }
            return JsonResponse(response_data)


        else:
            response_data = {
                'status':False,
                'message': 'Bad credentials!',
                'username': username,              
            }           
            return JsonResponse(response_data,status=400)
            
        
    return JsonResponse({
                'status':False,
                'message': 'Internal Server Error!',          
            },status=400)
    # return render(request, "authentication/signin.html")

@csrf_exempt
def signout(request):
    logout(request)
    return JsonResponse({
                'status':True,
                'message': "Logged Out Successfully!"         
            })


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        
        return render(request, 'activation_failed.html')

