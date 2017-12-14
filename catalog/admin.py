from django.contrib import admin
from .models import Book, Author, Genre, BookInstance
# from .models import MyModelName

#class MyModelNameAdmin(admin.ModelAdmin):
	#list_display = []
	#pass

# admin.site.register(MyModelName, MyModelNameAdmin)

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance)