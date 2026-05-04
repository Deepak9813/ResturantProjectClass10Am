from django.urls import path

# from main.views import indexPage, contactPage, aboutPage, menuPage, servicesPage
# from .views import indexPage, contactPage, aboutPage, menuPage, servicesPage
from .views import *

urlpatterns = [
    path('', indexPage, name='index_page'),
    path('contact/', contactPage, name='contact_page'),
    path('about/', aboutPage, name='about_page'),
    path('menu/', menuPage, name='menu_page'),
    path('services/', servicesPage, name='services_page'),
]
