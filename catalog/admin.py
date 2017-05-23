from django.contrib import admin

# Register your models here.
""" NOTE EVEN COMMENTS REQUIRE PROPER INDENTATION"""

from .models import Author, Genre, Book, BookInstance

class AuthorAdmin(admin.ModelAdmin):
	"""list_displays are headers for columns"""
	"""fields to display while adding a new one """

	list_display = ( 'date_of_birth','last_name', 'first_name','date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]  
"""To put closely related databases in same page for easier adding or editing use: TabularInline (horizontal layout), StackedInline (vertical). To create ModelInline and add it to Model Admin: inlines = .. """
class BookInstanceInline(admin.TabularInline):
	model = BookInstance
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BookInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
	"""fieldsets create subtitles & groups fields together in add a new row"""
	fieldsets = ((None, {'fields': ('book', 'imprint', 'id')}), ('Availabity', {'fields': ('status', 'due_back', 'borrower')}), )
	list_filter = ('status', 'due_back')  
	list_display = ('book', 'id', 'borrower','status', 'due_back')
	"""list_filter classifies files, videos, photos"""

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
