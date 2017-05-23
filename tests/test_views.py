from django.test import TestCase

from catalog.models import Author

class AuthorListViewTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		number_of_authors = 13
		for author_num in range(number_of_authors):
			Author.objects.create(first_name="Christian %s" % author_num, last_name="Surname %s" % author_num, )

	def test_view_url_exists_at_desired_location(self):
		resp = self.client.get('/catalog/author/')
		self.assertEqual(resp.status_code, 200)

	def test_view_uses_correct_template(self):
		resp = self.client.get(reverse('authors'))
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'catalog/author_list.html')

	def test_pagination_is_ten(self):
		resp = self.client.get(reverse('authors'))
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('is_paginated' in resp.context)
		self.assertTrue(resp.context['is_paginated'] == True)
		self.assertTrue( len(resp.context['author_list']) == 3)

	def test_lists_all_authors(self):
		#get second page and confirm it has the remaining 3 items
		resp = self.client.get(reverse('authors')+'?page=2')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('is_paginated' in resp.context)
		self.assertTrue(resp.context['is_paginated'] == True)
		self.assertTrue( len(resp.context['author_list']) == 3)

from catalog.models import Book, BookInstance, Genre
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import datetime
from django.utils import timezone

class LoanedBookInstancesByUserListViewTest(TestCase):

	def setUp(self):
		#create two users
		test_user1 = User.objects.create_user(username='testuser1', password='1234')
		test_user1.save()
		test_user2 = User.objects.create_user(username='testuser2', password='5678')
		test_user2.save()

		#create a book
		test_author = Author.objects.create(first_name='John', last_name='Smith')
		test_genre = Genre.objects.create(name='Fantasy')
		test_book = Book.objects.create(title='Book Title', summary='My book summary', isbn='ABCDE', author=test_author,  )

		#Adding extra information, create data for genre
		genre_objects_for_book = Genre.objects.all()
		test_book.genre = genre_objects_for_book
		test_book.save()

		#Create 30 BookInstance objects
		number_of_book_copies = 30
		for book_copy in range(number_of_book_copies):
			return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
			if book_copy % 2:
				the_borrower = test_user1
			else:
				the_borrower = test_user2
			status = 'm'
			BookInstance.objects.create(book=test_book, imprint='Unlikely, 2016', due_back=return_date, borrower=the_borrower, status=status)

	def test_redirect_if_not_logged_in(self):
		resp = self.client.get(reverse('borrowed'))
		self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')

	def test_logged_in_uses_correct_template(self):
		login = self.client.login(username="testuser1", password='1234')
		resp = self.client.get(reverse('borrowed'))

		#check our user is logged in
		self.assertEqual(str(resp.context['user']), 'testuser1')
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'catalog/borrower_list.html')

	def test_only_borrowed_books_in_list(self):
		login = self.client.login(username='testuser1', password='1234')
		resp = self.client.get(reverse('borrowed'))
		self.assertEqual(str(resp.context['user']), 'testuser1')
		self.assertEqual(resp.status_code, 200)

		#check that initially we don't books in list
		self.assertTrue('bookinstance_list' in resp.context)
		self.assertEqual( len(resp.context['bookinstance_list']), 0)

		#change all books to be on loan
		get_ten_books = BookInstance.objects.all()[:10]
		for copy in get_ten_books:
			copy.status = 'o'
			copy.save()

		resp = self.client.get(reverse('borrowed'))
		self.assertEqual(str(resp.context['user']), 'testuser1')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('bookinstance_list' in resp.context)

		#confirm all books belong to testuser1 and are on loan
		for bookitem in resp.context['bookinstance_list']:
			self.assertEqual(resp.context['user'], bookitem.borrower)
			self.assertEqual('o', bookitem.status)

		def test_pages_ordered_by_due_date(self):
			for copy in BookInstance.objects.all():
				copy.status = 'o'
				copy.save()

			login = self.client.login(username='testuser1', password='1234')
			resp = self.client.get(reverse('borrowed'))

			#check our user is logged in
			self.assertEqual(str(resp.context['user']), 'testuser1')
			self.assertEqual(resp.status_code, 200)
			self.assertEqual( len(resp.context['bookinstance_list']), 10)

			last_date = 0
			for copy in resp.context['bookinstance_list']:
				if last_date == 0:
					last_date = copy.due_back
				else: 
					self.assertTrue(last_date <= copy.due_back)

#tesing user permissions from views.RenewBookIntances()
from django.contrib.auth.models import Permission 

class RenewBookInstancesViewTest(TestCase):

	def setUp(self):
		test_user1 = User.objects.create_user(username="testuser1", password="1234")
		test_user1.save()

		test_user2 = User.objects.create_user(username="testuser2", password="5678")
		test_user2.save()
		permission = Permission.objects.get(name='Set book as returned')
		test_user2.user_permissions.add(permission)
		test_user2.save()

		#create book
		test_author = Author.objects.create(first_name="John", last_name="Smith")
		test_genre = Genre.objects.create(name='Fantasy')
		test_book = Book.objects.create(title='Book', summary="personal book", isbn = "Abcd", author=test_author, )
		genre_objects_for_book = Genre.objects.all()
		test_book.genre=genre_objects_for_book
		test_book.save()

		#Create Bookinstance for the un-permitted user1
		return_date = datetime.date.today() + datetime.timedelta(days=5)
		self.test_bookinstance1 = BookInstance.objects.create(book=test_book, imprint="unlikely imprint, 2016", due_back=return_date, borrower=test_user1, status='o')
		return_date = datetime.date.today() + datetime.timedelta(days=5)
		#create bookinstance for the permitted user2
		self.test_bookinstance2 = BookInstance.objects.create(book=test_book, imprint="Unlikely imprint, 2016", due_back=return_date, borrower=test_user2, status='o')
	def test_redirect_if_not_logged_in(self):
		resp = self.client.get(reverse('renew-book', kwargs={'pk': self.test_bookinstance1.pk, }))
		#manually check redirect, assertRedirect is for fixed urls
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(resp.url.startswith('/accounts/login/'))

	def test_redirect_if_logged_in_but_not_correct_permission(self):
		login = self.client.login(username='testuser1', password='1234')
		resp = self.client.get(reverse('renew-book', kwargs={'pk': self.test_bookinstance1.pk, }))
		self.assertEqual(resp.status_code, 302)
		self.assertTrue(resp.url.startswith('/accounts/login/'))

	def test_logged_in_with_permission_borrowed_book(self):
		login = self.client.login(username='testuser2', password='5678')
		resp = self.client.get(reverse('renew-book', kwargs={'pk': self.test_bookinstance2.pk, }))
		self.assertEqual( resp.status_code, 200)

	def test_logged_in_with_permission_another_users_borrowed_book(self):
		login = self.client.login(username='testuser2', password='5678')
		resp = self.client.get(reverse('renew-book', kwargs={'pk': self.test_bookinstance1.pk}))
		self.assertEqual( resp.status_code, 200)

	

	




