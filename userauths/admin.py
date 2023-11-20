from django.contrib import admin
from userauths.models import Profile, User, ContactUs

# this is to create a tabular representation of the users
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone']
    
admin.site.register(User, UserAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)