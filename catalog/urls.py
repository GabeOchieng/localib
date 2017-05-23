from django.conf.urls import url
from . import views
""" 
	each major feature should has a slug: home/author/, home/book/
	for home view the url: home/		index():base.html, index.html
	for list view the url: home/author	authors(): author_list.html
	for detail view the url: home/author/<id>	author.html
	for adding a new on: home/author/new       author():new_author.html  
	for editing a record: home/author/<id>/edit     #author_edit.html

"""


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^book/$', views.BookListView.as_view(), name='books'), 
	url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'), 
	url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book, name="renew-book"), 
	url(r'^author/$', views.AuthorListView.as_view(), name='authors'), 
	url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail' ), 
	url(r'^borrowed/$', views.all_borrowed, name='all-borrowed'),
	url(r'^borrowers/$', views.BookInstanceListView.as_view(), name="borrowers"), 

]
urlpatterns += [
	url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='borrowed'), 
]

urlpatterns += [
	url(r'^author/create/$', views.AuthorCreate.as_view(), name='author-create'), 
	url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author-update'), 
	url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author-delete'), 

]


