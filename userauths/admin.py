from django.contrib import admin
from userauths.models import User

# this is to create a tabular representation of the users
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',]
    
admin.site.register(User, UserAdmin)