from django.contrib import admin
from .models import MyModelName

class MyModelNameAdmin(admin.ModelAdmin):
	pass

admin.site.register(MyModelName, MyModelNameAdmin)
