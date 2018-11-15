from django.contrib import admin

# Register your models here.
from django.forms import Textarea

from .forms import PetitionAdmin
from .models import *
from django.db import models


admin.site.register(Comment)
admin.site.register(Story)
admin.site.register(UserWithProfile)
admin.site.register(Category)
admin.site.register(PetitionForAdmin)
admin.site.site_header = "Panel de administrador "
admin.site.site_title = "Wisapp"


class Admin(admin.ModelAdmin):
    # your stuff...
    formfield_overrides = {
        models.TextField: {'widget': Textarea},
    }
    class Media:
        css = {
            "all": ("styles.css")
        }
