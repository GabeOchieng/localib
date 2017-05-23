from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Examples:
    # url(r'^$', 'localib.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include('catalog.urls')), 
]

urlpatterns += [
	url(r'^$', RedirectView.as_view(url='/catalog/', permanent=True)), 
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
	url(r'^accounts/', include('django.contrib.auth.urls')), 
]




#ANOTHER WAY TO APPEND THE URLS
"""
urlpatterns = [
url(r'^admin/', admin.site.urls), 
url(r'^$', RedirectView.as_view(url='/catalog/', permanent=True)), 
  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  #Statics
"""
