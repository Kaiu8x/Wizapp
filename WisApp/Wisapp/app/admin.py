from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(UserWithProfile)
admin.site.register(Category)
#admin.site.register(Event)
admin.site.site_header = "Panel de administrador ";
admin.site.site_title = "Wisapp";