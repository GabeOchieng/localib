from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre

from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required, permission_required
import datetime
import re

from .forms import RenewBookForm

# Create your views here.

def index(request):
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count()   
	"""accceptable instead of: Author.objects.all().count()"""
	return render(request, 'catalog/index.html', context={'num_books': num_books, 'num_instances': num_instances, 'num_instances_available': num_instances_available, 'num_authors': num_authors}, )

class BookListView(LoginRequiredMixin, generic.ListView):
	model = Book
	login_url = '/accounts/login/'
	redirect_field_name = 'redirect_to'
	context_object_name = 'book_list'
	queryset = Book.objects.all()
	paginate_by = 2
	template_name = 'catalog/book_list.html'

class BookInstanceListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	login_url='/accounts/login/'
	redirect_field_name = 'next'
	context_object_name = 'bookinstance_list'
	paginate_by = 10
	template_name = 'catalog/borrower_list.html'

class BookDetailView(generic.DetailView):
	model = Book

class AuthorListView(generic.ListView):
	model = Author
	context_object_name = 'author_list'
	template = 'catalog/author_list.html'
	paginate_by = 3

class AuthorDetailView(generic.DetailView):
	model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/borrower_list.html'
	paginate_by = 2

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
		
@permission_required('catalog.can_mark_returned')
def all_borrowed(request):
	borrowed = BookInstance.objects.filter(status__exact='o').order_by('due_back')
	"""
	if request.method == "POST":
		book_status = request.POST.get("book_status")
		if re.match('return-(.*)', book_status):
			uuid = re.match('return-(.*)', book_status).group(1)
			inst = get_object_or_404(BookInstance, uuid)
			inst.due_back = "a"
			inst.save()
			return HttpResponseRedirect(reverse('all-borrowed'))
	"""


	return render(request, 'catalog/all_borrowed.html', {'borrowed': borrowed })



"""
		
		if book_status == "return":
				inst = get_object_or_404(BookInstance, pk)
				inst.status = "a"
				inst.save()
				return HttpResponseRedirect(reverse( 'all-borrowed' ) )

		else:
			return render(request, 'catalog/stuff.html', {'book_status': book_status })
	return HttpResponseRedirect(reverse('index'))

"""

@permission_required('catalog.can_mark_returned')
def renew_book(request, pk):
	book_inst = get_object_or_404(BookInstance, pk=pk)
	if request.method == 'POST':
		form = RenewBookForm(request.POST)
		if form.is_valid():
			book_inst.due_back = form.cleaned_data['renewal_date']
			book_inst.save()
			return HttpResponseRedirect(reverse('borrowers'))
	else: 
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })
	return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'book_inst': book_inst})

#GENERIC EDITING CRUD
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy  
#reversing for CBV use _lazy
from .models import Author

class AuthorCreate(CreateView):
	model = Author
	fields = '__all__'
	initial = {'date_of_death': '12/10/2015', }

class AuthorUpdate(UpdateView):
	model = Author
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
	model = Author
	success_url = reverse_lazy('authors')





