# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from authentication.models import User
from django.contrib import messages
from .forms import LoginForm, SignUpForm
from django.contrib.auth.hashers import make_password
from django.utils.decorators import decorator_from_middleware
from .middleware import *
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage,BadHeaderError
import secrets

# Define a decorator that excludes the middleware
exclude_middleware = decorator_from_middleware(PasswordChangeMiddleware)

@exclude_middleware
def redirect_login_view(request):
    return redirect('auth:login')

@exclude_middleware
def login_view(request):
    if request.user.is_authenticated :
        # Get the 'next' parameter from the query string
        next_url = request.GET.get('next', '/master/')
        return redirect(next_url)
     
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # check if the username exist in database
            try:
                User.objects.get(username=username)
            except:
                messages.error(request,'Username does not exist')

            # check the credential
            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request, user)
                # Get the 'next' parameter from the query string
                next_url = request.POST.get('next', '/master/')
                return redirect(next_url)
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):

    msg = None
    success = False
    print(request.POST)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'New user registered successfully !!'
            success = True
            # redirect to login view if user is registered
            return render(request, "accounts/register.html", {"form": SignUpForm(), "msg": msg,"status":success})

        else:
            msg = form.errors
            return render(request, "accounts/register.html", {"form": SignUpForm(), "msg": msg,"status":success})
    else:
        form = SignUpForm()

        return render(request, "accounts/register.html", {"form": SignUpForm(), "msg": msg,"status":success})


def password_change(request):
    if request.user.is_authenticated is False:
         return redirect("auth:login")
     
    if request.method == 'GET':
        return render(request, "accounts/password-change.html")
    
    else:
        msg=''
        # check if the username exist in database
        try:
            password1= request.POST.get('password')
            password2= request.POST.get('confirm_password')
            if password1 == password2:
                User.objects.filter(username=request.user).update(password=make_password(password1),is_password_changed=True)
                msg = 'Password Changed Successfully !!'
                return redirect('auth:logout')
            else:
                msg="Password doesn't match !!"    
            
        except Exception as e:
            print(e)
            msg ='Something is wrong !!'

    return render(request, "accounts/password-change.html", {"msg": msg})

@exclude_middleware
def forgot_password(request):
     
    if request.method == 'GET':
        return render(request, "accounts/forgot-password.html")
    else:
        msg=''
        # check if the username exist in database
        try:
            username= request.POST.get('username')
            user = User.objects.get(username=username)
            
            if user and user.email:
                subject = 'Applicaiton-Password Reset Link'
                from_email='test@gmail.com'
                
                recipient_list=[user.email]

                base_url = settings.BASE_URL
                
                token = secrets.token_hex(50 // 2)
                user.token = token
                user.save()
                message=''
                context ={
                    'user':user,
                    'base_url':base_url,
                    'token':token,
                }
                # Render the email content from the template
                email_content = render_to_string('email/password_reset_email.html', context)
                try:
                    
                    email = EmailMessage(subject, email_content, from_email, recipient_list)
                    email.content_subtype='html'
                    email.send()
                    msg = 'Password Reset Link sent on registered email !!'
                except BadHeaderError:
                    msg="Invalid header found in email."
                except Exception as e:
                    # Handle other exceptions (e.g., SMTP errors) here
                    msg = 'Error Occured !!'
                return redirect('auth:login')
            else:
                msg="Either Username doesn't match or E-mail is not configured !! Please Contact Administrator."    
            
        except Exception as e:
            print(e)
            msg =e

            return render(request, "accounts/forgot-password.html", {"msg": msg})
        
@exclude_middleware        
def forgot_password_confirm(request,token):
    user = User.objects.filter(token=token)
    if user.exists():
        user = user.first()
        if request.method == 'GET':
            context={
                'user':user,
            }
            return render(request,'accounts/password_reset_confirm.html',context)
        else:
            try:
                password1= request.POST.get('password')
                password2= request.POST.get('confirm_password')
                if password1 == password2:
                    user.password=make_password(password1)
                    user.is_password_changed=True
                    user.token=''
                    user.save()
                    
                    msg = 'Password Changed Successfully !!'
                    return redirect('auth:logout')
                else:
                    msg="Password doesn't match !!"    
                
            except Exception as e:
                print(e)
                msg ='Something is wrong !!'
            return render(request, "accounts/password_reset_confirm.html", {"msg": msg})
    else:
        msg="Token Expired !! Please Create New Request !!"
        return render(request, "accounts/forgot-password.html", {"msg": msg})
   
   
             

