from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Profile
from .models import Appointment
from .models import signup
from .models import data

admin.site.register(Appointment)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(signup)
admin.site.register(data)
