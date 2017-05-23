from django.test import TestCase
from catalog.models import Author

class AuthorModelTest(TestCase):
	#Field tests
	@classmethod

	def setUpTestData(cls):
		Author.objects.create(first_name='Big', last_name='Bob')

	def test_first_name_label(self):
		author = Author.objects.get(id=1)
		field_label = author._meta.get_field('first_name').verbose_name
		#in same way test .max_length
		self.assertEqual(field_label, 'first name')

	def test_object_name_is_last_name_comma_first_name(self):
		author = Author.objects.get(id=1)
		expected_object_name = '%s %s' %(author.first_name, author.last_name)
		self.assertEqual(expected_object_name, str(author) )
		#test __str__():

	def test_get_absolute_url(self):
		author = Author.objects.get(id=1)
		self.assertEqual(author.get_absolute_url(), '/catalog/author/1')






