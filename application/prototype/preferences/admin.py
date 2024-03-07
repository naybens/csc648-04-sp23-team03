from django.contrib import admin
from .models import Preference, Category, Choice, History

# Register your models here.
admin.site.register(Preference)
admin.site.register(Category)
admin.site.register(Choice)
admin.site.register(History)