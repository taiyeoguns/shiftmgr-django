from django.contrib import admin
from .models import Shift, Manager, Member

# Register your models here.
admin.site.register(Shift)
admin.site.register(Manager)
admin.site.register(Member)