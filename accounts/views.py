from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib import messages

from shop import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string


# Create your views here.
User = get_user_model()
def signup(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if User.objects.filter(username = username):
           messages.error(request, "Username already exist Please try some other username")
           return redirect('index')
       
        if User.objects.filter(email = email):
           messages.error(request, "Email already registered!")
           return redirect('index')    
       
        if len(username)> 10 :
            messages.error(request ,"Usernamemust be under 10 characters")
            
        if password != password1:
            messages.error(request , "Passwords didn't match!")
            
        if not username.isalnum():
            messages.error(request , "Username must be Alpha-Numerci")
            return redirect('index')    

        user = User.objects.create_user(username=username ,email=email,password=password)
        user.first_name = firstname
        user.save()
        messages.success(request, "Your Account has been successfully created .We have sent you a confirmation email")
        
        #Email
        subject = "Welcome to Shop -Django login"
        message = "Hello" + user.first_name + " Welcome Confiramtion Email"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject ,message , from_email, to_list , fail_silently=False)
        
        #Email confiramtion
        current_site  = get_current_site(request)
        email_subject = "Confirm your email"
        message2 = render_to_string('email_confirmation.html',{
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
            })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email]
            )
        email.fail_silently = False
        email.send()

        return redirect('login')
    
    return render(request, 'accounts/signup.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully ")
    return redirect('index')

def login_user(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username ,password=password)
        my_user = User.objects.get(username=username) 
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request , 'store/index.html', {'firstname':firstname})
        elif my_user.is_active == False:
            messages.error(request, "None Confirmation")
        
        else:
            messages.error(request, "Bad Credentials")    
            return redirect('login')
    
    return render(request, 'accounts/login.html')

def activate(request , uidb64 , token):
    try: 
        uid = force_text(urlsafe_base64_decode(uidb64)) 
      
        user = User.objects.get(pk = uid)
    except (TypeError , ValueError, OverflowError, User.DoesNotExist):
        user = None    
        
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()  
        messages.success(request, "Email activate")
        return redirect('login')  
    else:
        messages.error(request, "Failed activate")

        return redirect('index')
