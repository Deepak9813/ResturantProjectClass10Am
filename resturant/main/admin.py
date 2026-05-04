from django.contrib import admin
from .models import Contact, Category, Momo, Testimonial
from django.utils.html import format_html

# Register your models here.

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "phone_number", "email", "message"]
    ordering = ["id"]
    search_fields = ["full_name", "email", "phone_number"]





@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["id"]
    search_fields = ["name"]



@admin.register(Momo)
class MomoModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name","marked_price", "discount_percent", "selling_price", "selling_price1"]
    ordering = ["id"]
    search_fields = ["name"]



@admin.register(Testimonial)
class TestimonialModelAdmin(admin.ModelAdmin):
    # list_display = ["id", "full_name", 'bio', 'profile_picture_preview']
    list_display = ["id", "full_name", 'profile_picture_preview']
    ordering = ["id"]
    search_fields = ["id","full_name"]


    #to show profile picture
    def profile_picture_preview(self, obj):
            if obj.profile_pic:     #if True
                return format_html(
                    '<img src="{}" style="width: 50px; height:50px; border-radius:50%;" />',
                    obj.profile_pic.url
                )
            return "No Image"

    profile_picture_preview.short_description = "Profile Picture"