from django.db import models
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.core.urlresolvers import reverse    

from django.contrib.auth.models import User 
"""generates URLS by reversing them to connect list_display (html) to details_display

# Create your models here. 

class MyModelName(models.Model):
	my_field_name = models.CharField(max_length=20, help_text="Enter Field documentation")

	class Meta:
		ordering = ["-my_field_name"]

	def get_absolute_url(self):	
		#detailview the id or row in the db is accessed from the html 
		#page in a list items (row.get_absolute_url)
		return reverse('model-detail-view', args=[str(self.id)])  

	def __str__(self):
		return self.my_field_name
	

		#DetailView: shows one row or instance (has an id)
		#ListView: shows many rows or instances (all records)

	"""

class Genre(models.Model):
	name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, Poetry)")

	def __str__(self):
		return self.name


class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('Died', null=True, blank=True)

	def get_absolute_url(self):
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		return '%s %s' %(self.first_name, self.last_name)

class Book(models.Model):
	title= models.CharField(max_length=200)
	author= models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
	summary=models.TextField(max_length=1000, help_text="Enter a brief description")
	isbn = models.CharField('ISBN', max_length=13, help_text='13 character number')
	genre = models.ManyToManyField(Genre, help_text="Select a genre")

	def __str__(self):
		return self.title

	def display_genre(self): 
		"""to help list_display a ManyToManyField, show 3 values
		"""
		return ','.join([genre.name for genre in self.genre.all()[:3] ])
	display_genre.short_description = "Genre"

	def get_absolute_url(self):
		return reverse('book-detail', args=[str(self.id)])

	class Meta:
		permissions = (("can_certify", "Set as Quality"), )


class BookInstance(models.Model):
	"""uuid: produces unique keys"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for the book")
	book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)
	LOAN_STATUS = (
			('d', 'Maintainance'), 
			('o', 'on loan'), 
			('a', 'Available'), 
			('r', 'Reserved'), 
		)
	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='d', help_text='Book Availability')
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	class Meta:
		ordering = ["due_back"]
		permissions = (("can_mark_returned", "Set book as returned"), )

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False

	def __str__(self):
		return '%s (%s)' %(self.id, self.book)
"""
Every model change is followed by makemigrations and migrate
"""





