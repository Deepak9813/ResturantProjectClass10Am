import threading
# from threading import Thread

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Contact, Category, Momo, Testimonial

from resturant import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime

from django.contrib.auth.decorators import login_required

from django.utils import timezone

# Create your views here.

def indexPage(request):
    current_time = timezone.now()
    categories = Category.objects.all()
    testimonial = Testimonial.objects.all()

    #receve cate_id from url
    c_id = request.GET.get("cate_id")
    print("===================", print(type(c_id)))

    if c_id:    #if True
        #tyo category wala momo dekhaune(nikalne)
        momos = Momo.objects.filter(category=c_id)
    else:
         momos = Momo.objects.all()

    context = {
        "cate":categories,
        "momo":momos, "cat_id":c_id,
        "ct":current_time,
        "testi": testimonial
        }
   
    # return render(request, "main/index.html", {"cate":categories, "momo":momos, "cat_id":c_id, "ct":current_time})      #{"key":value} ==> dictionary(contexDictionary)
    return render(request, "main/index.html", context)      #{"key":value} ==> dictionary(contexDictionary)

def aboutPage(request):
    return render(request, "main/about.html")


'''
#simple main send
def contactPage(request):
    if request.method == "POST":
        #receive form data[i.e. data is received in the form of dictionary]
        data = request.POST
        #get(receive) individual data
        fl_name = data["fullName"]
        em = data["email"]
        phone = data["phoneNumber"]
        msg = data["mssg"]

        #save into data [create and save contact]
        Contact.objects.create(full_name=fl_name, email=em, phone_number=phone, message =msg)

        #send email
        subject = "Deepak Resturant"
        # message = "Thanks for contacting us"
        message = f""" 
                 Dear {fl_name},
                 Thanks for contacting us.

            """
        from_email = "deepakbaij2055@gmail.com" 
        recipient_list = [em]

        
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        # send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)

        # t1 = threading.Thread(target=send_mail,
        #                        args=(subject, message, from_email, recipient_list, False),
        #                         daemon=True
        #                         )
        # t1.start()

        t1 = threading.Thread(target=send_mail,
                               kwargs={
                                   "subject": subject,
                                   "message":message,
                                   "from_email": from_email,
                                    "recipient_list":recipient_list,
                                    "fail_silently":False
                               },
                               daemon=True
             )
        
        t1.start()

        messages.success(request, "Submitted successfully")
        # return redirect('contact_page')
        return redirect(reverse('contact_page')+'#helloDipak')
        

    return render(request, "main/contact.html")
'''


def contactPage(request):
    if request.method == "POST":
        #receive form data[i.e. data is received in the form of dictionary]
        data = request.POST
        #get(receive) individual data
        fl_name = data["fullName"]
        em = data["email"]
        phone = data["phoneNumber"]
        msg = data["mssg"]

        #save into data [create and save contact]
        Contact.objects.create(full_name=fl_name, email=em, phone_number=phone, message =msg)

        #======= send email with html file =====
        subject = "Deepak Momo Resturant"
        from_email = "deepakbaij2055@gmail.com"   #company email
        to = [em]           #jasle form varxa tesko email

        # First, render the plain text content.
        text_content = render_to_string("main/EmailMessage.html", {"fullName":fl_name, "date":datetime.now().year})   #{"key":"value"} 

        # Secondly, render the HTML content.
        # html_content =  render_to_string("main/EmailMessage.html", {"fullName":fl_name})   #{"key":"value"}
        html_content =  text_content

        # Then, create a multipart email instance. [i.e creating object of EmailMultiAlternatives]
        msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to)  

        #Lastly to remove html tags
        msg.attach_alternative(html_content , "text/html")
        # msg.send()  #send [for fast[background running use daemon]]

        t1 = threading.Thread(target=msg.send, daemon=True)
        t1.start()

        messages.success(request, "Submitted successfully")
        # return redirect('contact_page')
        return redirect(reverse('contact_page')+'#helloDipak')



    return render(request, "main/contact.html")




@login_required(login_url='login')          #name="login" wala
def menuPage(request):
    return render(request, "main/menu.html")

def servicesPage(request):
    return render(request, "main/services.html")