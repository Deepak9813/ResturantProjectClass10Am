from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from decimal import Decimal


# Create your models here.
class Contact(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    # phone_number = models.CharField(max_length=200)
    phone_number = PhoneNumberField(region="NP")
    message = models.TextField()

    class Meta:
        db_table = 'contact'
       


    #phone number field[terminal]:
        #pip install django-phonenumber-field[phonenumbers]





class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'
       



class Momo(models.Model):       #Momo===> Product
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_ho")
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="menu/")
    marked_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percent = models.IntegerField()
    selling_price = models.DecimalField(max_digits=8, decimal_places=2, editable=False)


    def save(self, *args, **kwargs):
        discount_amount = Decimal(self.discount_percent/100) * self.marked_price
        self.selling_price = self.marked_price - discount_amount

        return super().save(*args, **kwargs)
    
    @property
    def selling_price1(self):
        discount_amount = Decimal(self.discount_percent/100) * self.marked_price
        sp = self.marked_price - discount_amount
        # return sp
        return f"{sp:.2f}"

    

    class Meta:
        db_table = 'momo'
        


    


class Testimonial(models.Model):
    full_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='testimonial/')
    bio = models.TextField()


    class Meta:
        db_table = 'testimonial'

    




