import secrets
import threading

from django.shortcuts import render,redirect, get_object_or_404

from .models import CustomUser, Profile

from django.contrib import messages

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


from .models import Otp

from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

from django.urls import reverse



# Create your views here.
"""
def registerPage(request):
    if request.method == "POST":
        data = request.POST
        fname = data["fullName"]
        phone = data["phoneNumber"]
        uname = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirmPassword"]


        if password == confirm_password:
            if CustomUser.objects.filter(username=uname).exists():
                messages.error(request, "Username already exists")
                return redirect('register')
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('register')

            CustomUser.objects.create_user(full_name=fname, phone_number=phone, username=uname, email=email, password=password)
            messages.success(request, "Register successfully")
            return redirect('register')
        else:
            messages.error(request, "Password do not match")
            return redirect('register')         #url ko name = "register" waala register ho

    return render(request, "auth/Register.html")
"""

"""
#now including validation
def registerPage(request):
    if request.method == "POST":
        data = request.POST
        fname = data["fullName"]
        phone = data["phoneNumber"]
        uname = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirmPassword"]


        if password == confirm_password:
            try:
                validate_password(password)

                if CustomUser.objects.filter(username=uname).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                
                CustomUser.objects.create_user(full_name=fname, phone_number=phone, username=uname, email=email, password=password)
                messages.success(request, "Register successfully")
                return redirect('register')
            except ValidationError as e:
                for err in e.messages:
                    messages.error(request, err)
                return redirect('register')

        else:
            messages.error(request, "Password do not match")
            return redirect('register')         #url ko name = "register" waala register ho

    return render(request, "auth/Register.html")
"""
def registerPage(request):
    if request.method == "POST":
        data = request.POST
        fname = data["fullName"]
        phone = data["phoneNumber"]
        uname = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirmPassword"]


        if password == confirm_password:
            try:
                # user = CustomUser(full_name=fname, phone_number=phone, username=uname, email=email)
                # validate_password(password, user)
                validate_password(password)

                #for more validation
                if not re.search(r'[A-Z]', password):
                    messages.error(request, "Password must contain atleast one capital letter")
                    return redirect('register')
                
                if not re.search(r'\d', password):
                    messages.error(request, "Password must contain digit")
                    return redirect('register')
                
               #special character
                # Check for at least one special character[i.e. @, #, $, !, %, *, ^, +, =, ?, /, :, ;, etc., and underscore(_)]
                if not re.search(r'[\W_]', password):        # \W matches any non-word character (special characters)
                    messages.error(request, "Password must have atleast one special character!")
                    return redirect('register')

                if CustomUser.objects.filter(username=uname).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(phone_number=phone).exists():
                    messages.error(request, "Phone number already exists")
                    return redirect('register')
                
                CustomUser.objects.create_user(full_name=fname, phone_number=phone, username=uname, email=email, password=password)
                messages.success(request, "Register successfully")
                return redirect('register')
            except ValidationError as e:
                for err in e.messages:
                    messages.error(request, err)
                return redirect('register')

        else:
            messages.error(request, "Password do not match")
            return redirect('register')         #url ko name = "register" waala register ho

    return render(request, "auth/Register.html")


"""
def loginPage(request):
    if request.method == "POST":
        data = request.POST
        em = data["email"]
        psw = data["password"]

        # user = authenticate(request, email=em, password=psw)     #user(user object) or None
        user = authenticate(email=em, password=psw)     #user(user object) or None

        if user is not None:            #if user
            login(request,user)
            return redirect('menu_page')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, "auth/Login.html")

"""


def loginPage(request):
    if request.method == "POST":
        data = request.POST
        em = data["email"]
        psw = data["password"]

        remember_me = data.get("rem_me")
        # print("===================================", remember_me)

        # user = authenticate(request, email=em, password=psw)     #user(user object) or None
        user = authenticate(email=em, password=psw)     #user(user object) or None

        if user is not None:            #if user
            login(request,user)
            if remember_me:     #if True
                # request.session.set_expiry(22)      #add session     #login unitl 22 second but logout after 22 second
                request.session.set_expiry(86400)      #add session     #login for 1 day(i.e. 86400 second) but logout after 24 hour
            else:
                request.session.set_expiry(0)       #destrory session  #logout when browser close

            return redirect('menu_page')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, "auth/Login.html")





def logout_function(request):
    logout(request)
    messages.success(request, "logout successfully")
    return redirect('login')

@login_required(login_url="login")    
def changePassword(request):
    form = PasswordChangeForm(user=request.user)    
    if request.method == "POST":
        #receive form data
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password change sucessfully")
            return redirect('login')
    return render(request, "auth/ChangePassword.html", {"form":form})



"""
def resetPasswordEmailSend(request):
    if request.method == "POST":
        data = request.POST
        em = data["email"]

        #At first, check user exist or not using this email
        if not CustomUser.objects.filter(email=em).exists():
            messages.error(request, "Invalid email address")
            return redirect('reset_password_email_send')
        
                 
        user = CustomUser.objects.get(email=em)
        #Delete previous otp of this user
        # otp = Otp.objects.filter(user=user)
        # otp.delete()
        #===== in one line =========
        Otp.objects.filter(user=user).delete()
        
        #====== now generate otp in database and send it in email =======
        #======= generate 6 digit opt ==========
        otp = ''.join(secrets.choice("0123456789") for _ in range(6))
       #save into database
        Otp.objects.create(
            user=user,
            otp=otp,
            created_at=timezone.now(),
            expired_at=timezone.now()+timedelta(minutes=5)
        )
        #send email
        subject = "OTP Verification"
        message =  f'''
                    Your Otp is {otp}.
                    Please verify within 5 minute.
                    Do not share it with anyone.
                    '''

        from_email = "deepakbaij2055@gmail.com"
        recipient_list = [em]



        #send
        #send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
        t1 = threading.Thread(
            target=send_mail,
            args=(subject, message, from_email, recipient_list, False),
            daemon=True
        )
        t1.start()
        messages.success(request, "Otp sent successfully.\nPlease check email")
        
        # return redirect('verify_otp')

        #set user id in url parameter
        return redirect(reverse('verify_otp')+f"?user_id={user.id}")


    return render(request, "auth/reset-password/ResetPasswordEmailSend.html")



def verifyOtp(request):
    if request.method == "POST":
        data = request.POST
        otp = data["otp"]
        uid = data["userId"] 

        #find otp row(record) using this user and otp 
        user = CustomUser.objects.get(id=uid)
        otp_record = Otp.objects.filter(user=user, otp=otp).first()
        # otp_record = Otp.objects.filter(user=CustomUser.objects.get(id=uid), otp=otp) #in one line

        if not otp_record:      #if False    
            messages.error(request, "Invalid Otp")
            # return redirect('verify_otp')
            return redirect(reverse('verify_otp')+f"?user_id={user.id}")
        
        #check otp exipired or not
        current_time = timezone.now()
        if current_time>otp_record.expired_at:      #if current_time>expired_time
            otp_record.delete() #delete expired otp
            messages.error(request, "Otp expired")
            # messages.error(request, "Otp invalid")
            return redirect(reverse('verify_otp')+f"?user_id={user.id}")
        
        #==== otp valid case ===
        #first delete otp from database and then redirect to changepassword page
        otp_record.delete()
        # return redirect('reset_password')    
        return redirect(reverse('reset_password')+f"?user_id={user.id}")
    
    return render(request, "auth/reset-password/VerifyOtp.html")



def resetPassword(request):
    if request.method == "POST":
        data = request.POST
        psw = data["password"]
        confirm_password = data["confirmPassword"]
        uid = data["userId"]

        #find user using this id
        user = CustomUser.objects.get(id=uid)

        if psw == confirm_password:
            # user.password = psw
            user.set_password(psw)      #hash password   
            user.save()
            messages.success(request, "Password reset successfully")
            return redirect('login')
            
        else:
            messages.error(request, "Password do not match")
            return redirect(reverse('reset_password')+f"?user_id={user.id}")


    return render(request, "auth/reset-password/ResetPassword.html") 
    
"""




#======================== set user_id in session ========================

def resetPasswordEmailSend(request):
    if request.method == "POST":
        data = request.POST
        em = data["email"]

        #At first, check user exist or not using this email
        if not CustomUser.objects.filter(email=em).exists():
            messages.error(request, "Invalid email address")
            return redirect('reset_password_email_send')
        
                 
        user = CustomUser.objects.get(email=em)
        #Delete previous otp of this user
        # otp = Otp.objects.filter(user=user)
        # otp.delete()
        #===== in one line =========
        Otp.objects.filter(user=user).delete()
        
        #====== now generate otp in database and send it in email =======
        #======= generate 6 digit opt ==========
        otp = ''.join(secrets.choice("0123456789") for _ in range(6))
       #save into database
        Otp.objects.create(
            user=user,
            otp=otp,
            created_at=timezone.now(),
            expired_at=timezone.now()+timedelta(minutes=5)
        )
        #send email
        subject = "OTP Verification"
        message =  f'''
                    Your Otp is {otp}.
                    Please verify within 5 minute.
                    Do not share it with anyone.
                    '''

        from_email = "deepakbaij2055@gmail.com"
        recipient_list = [em]



        #send
        #send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
        t1 = threading.Thread(
            target=send_mail,
            args=(subject, message, from_email, recipient_list, False),
            daemon=True
        )
        t1.start()
        messages.success(request, "Otp sent successfully.\nPlease check email")
        
        

        #set user id in session
        request.session["user_id"] = user.id

        return redirect('verify_otp')
        # return redirect(reverse('verify_otp')+f"?user_id={user.id}")


    return render(request, "auth/reset-password/ResetPasswordEmailSend.html")



def verifyOtp(request):
    if request.method == "POST":
        data = request.POST
        otp = data["otp"]
        # uid = data["userId"]  #receive user id from form

        # receive user id  from session
        uid = request.session["user_id"]

        if not uid:
            messages.error(request, "session expired.. Please reset password again")
            return redirect('reset_password_email_send')
        
        #find otp row(record) using this user and otp 
        user = CustomUser.objects.get(id=uid)
        otp_record = Otp.objects.filter(user=user, otp=otp).first()
        # otp_record = Otp.objects.filter(user=CustomUser.objects.get(id=uid), otp=otp) #in one line

        if not otp_record:      #if False    
            messages.error(request, "Invalid Otp")
            return redirect('verify_otp')
            # return redirect(reverse('verify_otp')+f"?user_id={user.id}")
        
        #check otp exipired or not
        current_time = timezone.now()
        if current_time>otp_record.expired_at:      #if current_time>expired_time
            otp_record.delete() #delete expired otp
            messages.error(request, "Otp expired")
            # messages.error(request, "Otp invalid")
            return redirect('verify_otp')
            # return redirect(reverse('verify_otp')+f"?user_id={user.id}")
        
        #==== otp valid case ===
        #first delete otp from database and then redirect to changepassword page
        otp_record.delete()
        return redirect('reset_password')    
        # return redirect(reverse('reset_password')+f"?user_id={user.id}")
    
    return render(request, "auth/reset-password/VerifyOtp.html")




def resetPassword(request):
    if request.method == "POST":
        data = request.POST
        psw = data["password"]
        confirm_password = data["confirmPassword"]
        # uid = data["userId"]  #recevie user id from form

        #receive user id from session
        uid = request.session["user_id"]

        if not uid:
            messages.error(request, "session expired.. Please reset password again")
            return redirect('reset_password_email_send')

        #find user using this id
        user = CustomUser.objects.get(id=uid)

        if psw == confirm_password:
            # user.password = psw
            user.set_password(psw)      #hash password   
            user.save()
            messages.success(request, "Password reset successfully")
            return redirect('login')
            
        else:
            messages.error(request, "Password do not match")
            return redirect('reset_password')
            # return redirect(reverse('reset_password')+f"?user_id={user.id}")

    return render(request, "auth/reset-password/ResetPassword.html") 





#==================== profile ===================
@login_required(login_url='login')
def profilePage(request):
    # usr = request.user
    # profile,created = Profile.objects.get_or_create(user=usr)

    profile,created = Profile.objects.get_or_create(user=request.user)

    return render(request, "profile/Profile.html", {"pro":profile})


@login_required(login_url='login')
def editProfile(request):
    profile = Profile.objects.get(user=request.user)
    # profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        #receive form data
        data = request.POST
        fn = data["full_name"]
        uname = data["username"]
        em = data["email"]
        phone = data["phone_number"]
        gen = data["gender"]
        dob = data["date_of_birth"]

        #receive image
        pro_pic = request.FILES.get("profile_image")

        #find user and profile
        user = request.user
        # profile = Profile.objects.get(user=user)  #we already fetch(get) profile
        # profile = Profile.objects.get(user=request.user)


        #check unique things already exists or not
        #check email already exists or not
        


        #Set database data with incomming form data
        user.full_name = fn
        user.username = uname
        user.email = em
        user.phone_number = phone

        profile.gender = gen
        profile.date_of_birth = dob
        profile.updated_at = timezone.now()     #setting current time

        if pro_pic:     #if True
            profile.profile_pic = pro_pic

        #Now finally save user and profile into database
        user.save()
        profile.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile_page')
       

    return render(request, "profile/EditProfile.html", {"pro":profile})
    



    